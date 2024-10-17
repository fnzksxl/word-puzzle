import random
from collections import deque
from fastapi import Depends
from sqlalchemy.orm.session import Session
from typing import List, Tuple, Deque, Dict, Optional
from sqlalchemy import func

from app.models import WordInfo
from app.database import get_db


class PuzzleCreateService:
    def __init__(self, size: Optional[int] = None, db: Session = Depends(get_db)):
        """
        퍼즐의 크기를 받아 맵을 생성한다. 기본 값은 7x7
        Args:
            size (int or None): 퍼즐의 크기 + 1
        """
        self.db = db
        self.map_size = size + 1 if size is not None else 8
        self.map = self.create_map()
        self.queue = deque()
        self.desc = []
        self.words = []
        self.num = 2
        self.word_size = 494047

    def create_map(self) -> List[str]:
        """
        0으로 초기화 된 맵을 생성해 반환한다.
        """
        return [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]

    async def append_letter_into_queue(
        self, start_point: Tuple[int, int], length: int, word: str, dir: bool
    ) -> Deque:
        """
        시작점, 길이, 단어, 방향을 토대로 큐에 다음 단어 추가에 대한 힌트를 큐에 삽입 후 반환한다.

        Args:
            start_point (Tuple): 단어 첫 음절이 위치하는 곳
            length (int): 단어의 길이
            word (str): 단어
            dir (bool): 단어 방향 가로, 세로 여부
        Returns:
            Deque: 다음 단어의 시작점, 시작 음절, 방향이 추가된 큐
        """

        def add_to_queue(coord: Tuple[int, int], letter: str, dir: bool) -> None:
            if 0 <= coord[0] < self.map_size and 0 <= coord[1] < self.map_size:
                self.queue.append(((coord[0], coord[1]), letter, not (dir)))

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

        return self.queue

    async def find_first_word_info(self) -> WordInfo:
        """
        DB에서 랜덤으로 하나의 단어를 찾아 반환한다.

        Returns:
            WordInfo: 랜덤으로 가져온 WordInfo Row 객체
        """
        random_idx = random.randint(1, self.word_size)
        return self.db.query(WordInfo).filter(WordInfo.id == random_idx).first()

    async def find_word_info_start_with(self, start_word: str, limit: int) -> WordInfo:
        """
        DB에서 {start_word}로 시작하면서 길이가 limit 이하인 단어를 찾아 반환한다.
        Args:
            start_word (str): 시작 어절
            limit (int): 가능한 최대 길이
        Returns:
            WordInfo: {start_word}로 시작하면서 길이가 limit 이하인 WordInfo Row 객체
        """
        return (
            self.db.query(WordInfo)
            .filter(WordInfo.word.like(f"{start_word}%"))
            .filter(WordInfo.len <= limit)
            .order_by(func.rand())
            .first()
        )

    async def create_puzzle_phase1(self) -> None:
        """
        0으로 초기화 된 맵에 첫 단어를 추가,
        이 후 추가될 단어와 그 위치에 대한 힌트를 큐에 삽입,
        첫 단어 설명 추가
        """
        word = await self.find_first_word_info()
        start_y, start_x = 0, 0

        for i in range(word.len):
            self.map[start_y][start_x + i] = 1

        self.words.append({"num": 1, "word": word.word})
        self.desc.append({"num": 1, "desc": word.desc})
        self.queue = await self.append_letter_into_queue(
            (start_y, start_x), word.len, word.word, True
        )

    async def inspect_possible_length(
        self, point: Tuple[int, int], dir: bool, phase: int = 2
    ) -> int:
        """
        단어의 시작 좌표와 방향으로 가능한 단어의 최대 길이를 반환한다.

        Args:
            point (Tuple[int,int]): 단어가 시작될 좌표
            dir (bool): 단어의 가로, 세로 여부
            phase (int): 퍼즐 생성 단계
        Returns:
            int: 가능한 단어의 길이
        """
        y, x = point

        if phase == 3:
            if y > 0 and self.map[y - 1][x] != 0:
                return 0
            if y < self.map_size - 1 and self.map[y + 1][x] != 0:
                return 0
            if x > 0 and self.map[y][x - 1] != 0:
                return 0
            if x < self.map_size - 1 and self.map[y][x + 1] != 0:
                return 0
        if x >= 1:
            if dir and self.map[y][x - 1] != 0:
                return 0
        if y >= 1:
            if not dir and self.map[y - 1][x] != 0:
                return 0

        if dir:
            for i in range(1, 5):
                if (
                    (y - 1 >= 0 and self.map[y - 1][x + i] != 0)
                    or (y + 1 < self.map_size and self.map[y + 1][x + i] != 0)
                    or (x + i < self.map_size - 1 and self.map[y][x + i + 1] != 0)
                    or (x + i == self.map_size - 1)
                ):
                    return i
        else:
            for i in range(1, 5):
                if (
                    (x - 1 >= 0 and self.map[y + i][x - 1] != 0)
                    or (x + 1 < self.map_size and self.map[y + i][x + 1] != 0)
                    or (y + i < self.map_size - 1 and self.map[y + i + 1][x] != 0)
                    or (y + i == self.map_size - 1)
                ):
                    return i

        return 5

    async def fill_puzzle_until_queue_empty(self) -> None:
        """
        큐가 빌 때까지 퍼즐에 단어를 추가시킨다.
        """
        while self.queue:
            point, start_word, dir = self.queue.popleft()
            limit = await self.inspect_possible_length(point, dir)

            if limit <= 1:
                continue
            next_word = await self.find_word_info_start_with(start_word, limit)

            if not next_word:
                continue
            for i in range(next_word.len):
                if dir:
                    self.map[point[0]][point[1] + i] = self.num
                else:
                    self.map[point[0] + i][point[1]] = self.num

            self.words.append({"num": self.num, "word": next_word.word})
            self.desc.append({"num": self.num, "desc": next_word.desc})
            self.num += 1

            self.queue = await self.append_letter_into_queue(
                point, next_word.len, next_word.word, dir
            )

    async def create_puzzle_phase2(self) -> None:
        """
        단어 하나가 삽입된 상태에서, 시작 어절이 같은 단어를 찾아 추가한다.
        단, 진행방향의 삼면에 이미 다른 단어의 어절이 없어야 한다.
        이 함수는 두 번째 페이즈로, 처음 추가된 단어와 이어지는 경우에만 단어를 추가한다.
        """
        await self.create_puzzle_phase1()
        await self.fill_puzzle_until_queue_empty()

    async def create_puzzle_phase3(self) -> Dict:
        """
        퍼즐의 비어있는 공간에 단어를 추가한다.
        Returns:
            Returns:
            Dict: 맵, 설명 및 단어가 들어있는 사전형 자료
        """
        await self.create_puzzle_phase2()
        for i in range(self.map_size - 1):
            for j in range(self.map_size - 1):
                if self.map[i][j] == 0:
                    hor = await self.inspect_possible_length((i, j), True, phase=3)
                    ver = await self.inspect_possible_length((i, j), False, phase=3)
                    dir = True if hor > ver else False
                    if not (hor and ver):
                        continue
                    else:
                        word = await self.find_word_info_start_with("", hor if hor > ver else ver)
                        if not word:
                            continue
                        for k in range(word.len):
                            if dir:
                                self.map[i][j + k] = self.num
                            else:
                                self.map[i + k][j] = self.num

                        self.words.append({"num": self.num, "word": word.word})
                        self.desc.append({"num": self.num, "desc": word.desc})
                        self.num += 1
                        self.queue = await self.append_letter_into_queue(
                            (i, j), word.len, word.word, dir
                        )
                        await self.fill_puzzle_until_queue_empty()

        return {"map": self.map, "desc": self.desc, "words": self.words}
