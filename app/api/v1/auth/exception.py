from fastapi import HTTPException


class LoginNotValidIDPWException(HTTPException):
    def __init__(self, detail: str = "입력한 ID 또는 비밀번호가 일치하지 않습니다."):
        super().__init__(status_code=400, detail=detail)


class GoogleGetTokenException(HTTPException):
    def __init__(self, detail: str = "구글 토큰 획득 과정에서 오류가 발생했습니다."):
        super().__init__(status_code=400, detail=detail)


class GoogleGetUserInfoException(HTTPException):
    def __init__(self, detail: str = "구글 유저 정보 과정에서 오류가 발생했습니다."):
        super().__init__(status_code=400, detail=detail)


class GoogleRegisterException(HTTPException):
    def __init__(self, detail: str = "구글 소셜 회원가입 과정에서 오류가 발생했습니다."):
        super().__init__(status_code=400, detail=detail)
