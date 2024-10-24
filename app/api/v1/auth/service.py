import bcrypt
import httpx

from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from fastapi import Depends
from typing import Optional, Dict

from app.config import settings
from app.database import get_db
from app.models import User, OAuth
from .auth import AuthBase, OAuthBase
from .exception import (
    GoogleRegisterException,
    GoogleGetTokenException,
    GoogleGetUserInfoException,
    LoginNotValidIDPWException,
)


class GeneralAuthService(AuthBase):
    """
    아이디(이메일), 비밀번호로 회원가입/로그인, 인증 서비스 클래스
    """

    def __init__(self, email: str, password: str, nickname: str, db: Session):
        """
        입력받은 이메일, 비밀번호, 닉네임을 초기화한다.
        """
        self.email = email
        self.password = password
        self.nickname = nickname
        self.db = db
        super().__init__()

    async def register(self) -> Dict:
        """
        비밀번호를 해쉬화해서 데이터베이스에 유저 정보를 저장하는 메소드

        Returns:
            dict: 필요한 유저 정보만 담아 반환되는 딕셔너리 자료
        """
        user = User(email=self.email, password=await self._hash_pw(), nickname=self.nickname)
        self.db.add(user)
        self.db.commit()
        user_dict = user.as_dict()
        user_dict.pop("password")
        return {"user": user_dict}

    async def login(self) -> JSONResponse:
        """
        이메일과 비밀번호로 유저 정보를 확인하여 로그인하는 메소드

        Returns:
            JSONResponse: 쿠키에 토큰 정보, 콘텐츠에 유저 정보를 담은 response 객체
        """
        user = self.db.query(User).filter(User.email == self.email).first()
        if user and bcrypt.checkpw(self.password.encode(), user.password.encode()):
            return await self._get_login_response(user)
        raise LoginNotValidIDPWException()

    async def _hash_pw(self) -> str:
        """
        비밀번호를 해쉬화 해 반환한다.

        Returns:
            str: 해쉬화 된 비밀번호
        """
        salt_value = bcrypt.gensalt()
        return bcrypt.hashpw(self.password.encode(), salt_value)


class GoogleOAuthService(OAuthBase):
    def __init__(self, code: str, db: Session = Depends(get_db)):
        """
        구글 소셜 로그인에 필요한 정보를 초기화 한다.
        """
        super().__init__()
        self.provider = "google"
        self.client_id = settings.GOOGLE_CLIENT_ID
        self.redirect_uri = settings.GOOGLE_REDIRECT_URI
        self.client_secret = settings.GOOGLE_CLIENT_SECRET
        self.db = db
        self.code = code
        self.token_request_url = "https://oauth2.googleapis.com/token"
        self.userinfo_endpoint = "https://www.googleapis.com/userinfo/v2/me"

    async def register(self) -> JSONResponse:
        try:
            user = User(email=self.oauth_user_info.get("email", None), nickname="gimozzi")
            self.db.add(user)
            self.db.flush()

            oauth = OAuth(user_id=user.id, email=user.email, provider=self.provider)
            self.db.add(oauth)

            self.db.commit()
        except Exception:
            raise GoogleRegisterException()

        return await self._get_login_response(user)

    async def login(self) -> JSONResponse:
        """
        소셜 로그인 로직을 수행하는 기초 메소드,
        데이터베이스에 유저 존재 -> 정보 반환
        존재 X -> 저장(회원가입) 후 정보 반환

        Returns:
            JSONResponse: 쿠키에 토큰 정보, 콘텐츠에 유저 정보를 담은 response 객체
        """
        user = await self.is_registered()

        if user is None:
            return await self.register()

        return await self._get_login_response(user)

    async def get_token(self) -> str:
        """
        유저 정보 조회에 필요한 토큰을 받아온다.

        Returns:
            str: 구글 OAuth 서비스에서 받은 토큰
        """
        token_request_payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "code": self.code,
            "client_secret": self.client_secret,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.token_request_url, data=token_request_payload)
        result = response.json()

        if "access_token" in result:
            return result["access_token"]
        else:
            raise GoogleGetTokenException()

    async def get_userinfo(self, token) -> Dict:
        """
        구글에서 받아온 토큰으로 유저 정보를 요청하고 반환한다.

        Args:
            token (str): 구글에서 받아온 토큰
        Returns:
            dict:
        """
        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.userinfo_endpoint, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise GoogleGetUserInfoException()

    async def is_registered(self) -> Optional[User]:
        """
        가입된 유저라면 유저 정보를, 아니라면 None을 반환한다.

        Returns:
            User or None: 정보가 있다면 User 객체, 아니면 None 반환
        """
        token = await self.get_token()
        user_info = await self.get_userinfo(token)
        return await self.get_user_from_db(user_info)

    async def get_user_from_db(self, user_info):
        """
        구글에서 받은 유저 정보를 데이터베이스에 검색하고
        존재하면 User 객체, 아니면 None을 반환한다.

        Args:
            user_info (dict): 구글에서 받은 유저 정보
        Returns:
            User or None: 정보가 있다면 User 객체, 아니면 None 반환
        """
        oauth_user_info = (
            self.db.query(OAuth)
            .filter(OAuth.provider == self.provider, OAuth.email == user_info.get("email", None))
            .first()
        )
        if oauth_user_info:
            user = self.db.query(User).filter(User.id == oauth_user_info.user_id).first()
            return user
        self.oauth_user_info = user_info
        return None
