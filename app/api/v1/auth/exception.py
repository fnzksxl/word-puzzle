from fastapi import HTTPException


class EmailDuplicatedException(HTTPException):
    def __init__(self, detail: str = "중복된 이메일입니다."):
        super().__init__(status_code=400, detail=detail)


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


class TokenExpiredException(HTTPException):
    def __init__(self, detail: str = "만료된 토큰입니다."):
        super().__init__(status_code=401, detail=detail)


class TokenNotExistException(HTTPException):
    def __init__(self, detail: str = "토큰이 존재하지 않습니다."):
        super().__init__(status_code=400, detail=detail)
