from datetime import timedelta, datetime
from zoneinfo import ZoneInfo
from jose import jwt, JWTError
from typing import Optional, Dict

from app.config import settings


class JWTService:
    """
    JWT 암호화 및 해독에 필요한 기능을 제공하는 클래스
    """

    def __init__(self):
        self.algorithm = settings.ALGORITHM
        self.secret_key = settings.SECRET_KEY
        self.access_expire_time = settings.ACCESS_EXPIRE_TIME
        self.refresh_expire_time = settings.REFRESH_EXPIRE_TIME

    def _encode(self, data: dict, expires_delta: int) -> str:
        """
        JWT 토큰으로 암호화한다.

        Args:
            data (dict): 암호화 할 데이터
            expires_delta (int): JWT 만료기간
        Returns:
            str: JWT 토큰
        """
        to_encode = data.copy()
        expire = datetime.now(ZoneInfo("Asia/Seoul")) + timedelta(minutes=expires_delta)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def _decode(self, token: str) -> Optional[Dict]:
        """
        JWT 토큰을 해독한다.

        Args:
            token (str): JWT 토큰
        Returns:
            Dict or None: 해독 성공 시 정보를 담은 사전, 실패 시 None
        """
        try:
            return jwt.decode(token, self.secret_key, algorithm=self.algorithm)
        except JWTError:
            return None

    def _create_token(self, data: dict, expires_delta: int) -> str:
        """
        JWT 토큰 암호화 래퍼함수
        """
        return self._encode(data, expires_delta)

    def create_access_token(self, data) -> str:
        """
        Access Token 생성 함수
        """
        return self._create_token(data, self.access_expire_time)

    def create_refresh_token(self, data) -> str:
        """
        Refresh Token 생성 함수
        """
        return self._create_token(data, self.refresh_expire_time)

    def check_is_expired(self, token: str) -> Optional[Dict]:
        """
        JWT 토큰 해독 래퍼함수
        """
        payload = self._decode(token, self.secret_key, self.algorithm)

        now = datetime.timestamp(datetime.now(ZoneInfo("Asia/Seoul")))
        if payload and payload["exp"] < now:
            return None

        return payload
