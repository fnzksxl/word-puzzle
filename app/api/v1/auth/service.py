import bcrypt

from fastapi.responses import JSONResponse
from sqlalchemy.orm.session import Session
from typing import Dict

from app.models import User
from .auth import AuthBase
from .exception import LoginNotValidIDPWException


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
