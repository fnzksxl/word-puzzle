from abc import ABC, abstractmethod
from fastapi.responses import JSONResponse

from .jwt import JWTService
from .cookie import Cookie


class AuthBase(ABC):
    """
    AuthService의 기초가 되는 추상클래스
    """

    def __init__(self):
        self.jwt_service = JWTService()
        self.cookie_service = Cookie()

    @abstractmethod
    async def register(self):
        """
        회원가입을 담당하는 추상 메소드
        """
        pass

    @abstractmethod
    async def login(self):
        """
        로그인을 담당하는 추상 메소드
        """
        pass

    async def _get_login_response(self, user) -> JSONResponse:
        """
        로그인 성공 후 응답을 생성하는 메소드
        Args:
            user (User): 로그인한 유저의 User 객체
        Returns:
            JSONResponse: Access, Refresh Token이 쿠키에 들어간 응답
        """
        self.user_dict = user.as_dict()
        self.user_dict.pop("password")
        self.user_dict.pop("created_at")
        self.user_dict.pop("updated_at")

        response = JSONResponse(content=self.user_dict)
        return await self._attach_token(response, self.user_dict)

    async def _attach_token(self, response, data) -> JSONResponse:
        """
        응답 쿠키에 Access, Refresh Token을 부착하는 메소드
        Args:
            response (JSONResponse): content로 유저 정보가 들어간 응답 객체
            data: Access, Refresh Token
        Returns:
            JSONResponse: Access, Refresh Token이 쿠키에 들어간 응답
        """
        access_token = self.jwt_service.create_access_token(data)
        refresh_token = self.jwt_service.create_refresh_token(data)
        return await self.cookie_service.attach_token_into_cookie(
            response, access_token, refresh_token
        )
