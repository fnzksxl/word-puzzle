from fastapi import HTTPException


class AlreadySolvedPuzzleExepction(HTTPException):
    def __init__(self, detail: str = "이미 해결한 문제입니다."):
        super().__init__(status_code=400, detail=detail)
