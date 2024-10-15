from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import WordInfo

import re
import os
import json
from app.config import settings


DIR = os.getcwd()
DATA_DIR = DIR + "/word-data"
json_list = os.listdir(DATA_DIR)

def process_word(word):
    """
    자음이 포함된 단어 제거, 단어에 한글을 제외한 문자 및 공백 제거, 지정 길이를 벗어나는 단어 제거
    위 세 가지 일을 한 뒤 단어와 그 길이를 반환합니다

    Args:
        word (str): 정제할 단어
    Returns:
        dict: {단어, 단어의 길이}
    """
    word = word.strip()
    consonant_mixed = re.search(r'[ㄱ-ㅎ]', word)
    
    if consonant_mixed:
        return None
    
    result = re.sub(r'[^가-힣]', '', word)
    length = len(result)
    if length > 7 or length < 2:
        return None
    
    return {"word": result, "length": length}

def process_senseinfo(senseinfo):
    """
    단어의 품사가 없거나 '품사 없음'일 시 제거, 방언 및 북한어 제거, 설명에 특이점이 있으면 제거
    위 세 가지 일을 한 뒤 설명과 단어의 품사를 반환합니다

    Args:
        senseinfo (dict): 품사, 설명 데이터가 들어있는 딕셔너리
    Returns:
        dict: {설명, 품사}
    """
    definition = senseinfo["definition"].strip()
    word_type = senseinfo["type"].strip()
    pos = senseinfo.get("pos", None)

    if pos is None or pos == "품사 없음":
        return None
    
    if word_type == "방언" or word_type == "북한어":
        return None
    
    if len(definition) > 200 or "&" in definition or "img" in definition or "<FL>" in definition or "규범 표기" in definition or "준말" in definition or "옛말" in definition or "-" in definition:
        return None
    
    return {"definition": definition, "pos": pos}

if __name__ == "__main__":
    """
    JSON 파일로부터 단어 로우 데이터를 읽어들이고, 정제한 뒤 WordInfo 테이블에 추가합니다.
    """
    engine = create_engine(
    "mysql+pymysql://{username}:{password}@{host}:{port}/{name}".format(
        username=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        name=settings.DB_NAME,
        )
    )

    Session = sessionmaker(bind=engine)
    db = Session()
    word_list = []

    for i, _json in enumerate(json_list):
        print(f"{len(json_list)}/{i+1}번 째 파일, 파일명 : {_json}")
        with open(DATA_DIR+"/"+_json, encoding="utf-8") as f:
            json_data = json.load(f)
            for word_data in json_data["channel"]["item"]:
                processed_word = process_word(word_data["wordinfo"]["word"])
                processed_senseinfo = process_senseinfo(word_data["senseinfo"])
                if processed_word and processed_senseinfo:
                    word_list.append({
                        "word": processed_word["word"],
                        "desc": processed_senseinfo["definition"],
                        "pos": processed_senseinfo["pos"],
                        "len": processed_word["length"]
                    })
                else:
                    continue
            print(f"현재 단어 수 : {len(word_list)}")

    db.bulk_insert_mappings(WordInfo, word_list)
    db.commit()

    db.close()