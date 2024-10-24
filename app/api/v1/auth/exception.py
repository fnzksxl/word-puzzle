from fastapi import HTTPException


class LoginNotValidIDPWException(HTTPException):
    def __init__(self, detail: str = "입력한 ID 또는 비밀번호가 일치하지 않습니다."):
        super().__init__(status_code=400, detail=detail)
