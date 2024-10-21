from fastapi import HTTPException


class PuzzleNotExistException(HTTPException):
    def __init__(self, detail: str = "존재하지 않는 퍼즐입니다."):
        super().__init__(status_code=404, detail=detail)
