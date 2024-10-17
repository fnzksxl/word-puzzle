import random
from collections import deque
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm.session import Session
from typing import List, Tuple, Deque, Dict

from app.models import WordInfo
from app.database import get_db


async def append_letter_into_queue(
    start_point: Tuple[int, int], length: int, word: str, queue: deque, dir: bool
) -> Deque:
    """
    시작점, 길이, 단어, 방향을 토대로 큐에 다음 단어 추가에 대한 힌트를 큐에 삽입 후 반환한다.

    Args:
        start_point (Tuple): 단어 첫 음절이 위치하는 곳
        length (int): 단어의 길이
        word (str): 단어
        queue (deque): 큐
        dir (bool): 단어 방향 가로, 세로 여부
    Returns:
        Deque: 다음 단어의 시작점, 시작 음절, 방향이 추가된 큐
    """

    def add_to_queue(coord: Tuple[int, int], letter: str, dir: bool) -> None:
        if 0 <= coord[0] < 11 and 0 <= coord[1] < 11:
            queue.append(((coord[0], coord[1]), letter, not (dir)))

    if dir:
        add_to_queue((start_point[0], start_point[1] + length - 1), word[-1], dir)
    else:
        add_to_queue((start_point[0] + length - 1, start_point[1]), word[-1], dir)

    if length > 2:
        if length >= 5:
            if dir:
                add_to_queue((start_point[0], start_point[1] + 2), word[2], dir)
            else:
                add_to_queue((start_point[0] + 2, start_point[1]), word[2], dir)
        add_to_queue(start_point, word[0], dir)

    return queue


async def create_map() -> List[str]:
    """
    0으로 초기화 된 맵을 생성해 반환한다.
    Args:
        None
    Returns:
        List[str]
    """
    map = [[0 for _ in range(11)] for _ in range(11)]
    return map


async def find_first_word_info(db: Session = Depends(get_db)) -> WordInfo:
    """
    DB에서 랜덤으로 하나의 단어를 찾아 반환한다.
    Args:
        db (Session): 커넥션
    Returns:
        WordInfo: 랜덤으로 가져온 WordInfo Row 객체
    """
    random_idx = random.randint(1, 494047)
    return db.query(WordInfo).filter(WordInfo.id == random_idx).first()


async def find_word_info_start_with(start_word: str, db: Session) -> WordInfo:
    """
    DB에서 {start_word}로 시작하는 단어를 찾아 반환한다.
    Args:
        db (Session): 커넥션
        start_word (str): 시작 어절
    Returns:
        WordInfo: {start_word}로 시작하는 WordInfo Row 객체
    """
    return (
        db.query(WordInfo)
        .filter(WordInfo.word.like(f"{start_word}%"))
        .order_by(func.rand())
        .first()
    )


async def create_puzzle_phase1(
    word: WordInfo = Depends(find_first_word_info), map: List[str] = Depends(create_map)
) -> Dict:
    """
    0으로 초기화 된 맵에 첫 단어를 추가,
    이 후 추가될 단어와 그 위치에 대한 힌트를 큐에 삽입,
    첫 단어 설명 추가 후 반환한다.

    Args:
        word (WordInfo): 단어 정보
        map (List[str]): 0으로 초기화 된 맵
    Returns:
        Dict: {map(List[str]), queue(deque), desc(dict)}
    """
    start_y, start_x = 0, 0
    queue = deque()
    desc = []
    words = []
    for i in range(word.len):
        map[start_y][start_x + i] = 1

    words.append({"num": 1, "word": word.word})
    desc.append({"num": 1, "desc": word.desc})
    queue = await append_letter_into_queue((start_y, start_x), word.len, word.word, queue, True)

    return {"map": map, "queue": queue, "desc": desc, "words": words}


async def create_puzzle_phase2(
    db: Session = Depends(get_db), map_queue_desc: Dict = Depends(create_puzzle_phase1)
) -> Dict:
    """
    단어 하나가 삽입된 상태에서, 시작 어절이 같은 단어를 찾아 추가한다.
    단, 진행방향의 삼면에 이미 다른 단어의 어절이 없어야 한다.
    이 함수는 두 번째 페이즈로, 처음 추가된 단어와 이어지는 경우에만 단어를 추가한다.

    Args:
        db (Session): 커넥션
        map_queue_desc (Dict): 맵, 큐, 설명 및 단어가 들어있는 사전형 자료
    Returns:
        Dict: 맵, 큐, 설명 및 단어가 들어있는 사전형 자료
    """
    map = map_queue_desc.get("map")
    queue = map_queue_desc.get("queue")
    desc = map_queue_desc.get("desc")
    words = map_queue_desc.get("words")
    num = 2
    while queue:
        point, start_word, dir = queue.popleft()
        next_word = await find_word_info_start_with(start_word, db)
        if not next_word:
            continue
        if (next_word) and (
            (dir and point[1] + next_word.len < 11) or (not dir and point[0] + next_word.len < 11)
        ):
            if point[1] >= 1:
                if dir and map[point[0]][point[1] - 1] != 0:
                    continue
            if point[0] >= 1:
                if not dir and map[point[0] - 1][point[1]] != 0:
                    continue

            original_value = map[point[0]][point[1]]
            for i in range(next_word.len):
                if dir:
                    if i and map[point[0]][point[1] + i] != 0:
                        for j in range(i):
                            map[point[0]][point[1] + j] = original_value
                        break
                    if i and (
                        (point[1] + i + 1 < 11 and map[point[0]][point[1] + i + 1] != 0)
                        or (point[0] - 1 >= 0 and map[point[0] - 1][point[1] + i] != 0)
                        or (point[0] + 1 < 11 and map[point[0] + 1][point[1] + i] != 0)
                    ):
                        for j in range(1, i):
                            map[point[0]][point[1] + j] = 0
                        map[point[0]][point[1]] = original_value
                        break

                    map[point[0]][point[1] + i] = num
                else:
                    if i and map[point[0] + i][point[1]] != 0:
                        for j in range(i):
                            map[point[0] + j][point[1]] = original_value
                        break
                    if i and (
                        (point[1] - 1 >= 0 and map[point[0] + i][point[1] - 1] != 0)
                        or (point[1] + 1 < 11 and map[point[0] + i][point[1] + 1] != 0)
                        or (point[0] + i + 1 < 11 and map[point[0] + i + 1][point[1]] != 0)
                    ):
                        for j in range(1, i):
                            map[point[0] + j][point[1]] = 0
                        map[point[0]][point[1]] = original_value
                        break
                    map[point[0] + i][point[1]] = num

            else:
                words.append({"num": num, "word": next_word.word})
                desc.append({"num": num, "desc": next_word.desc})
                num += 1

                queue = await append_letter_into_queue(
                    point, next_word.len, next_word.word, queue, dir
                )
    return {"map": map, "desc": desc, "words": words}
