from fastapi.responses import JSONResponse


class Cookie:
    """
    응답 객체의 쿠키 관련 작업을 담당하는 클래스
    """

    async def attach_token_into_cookie(
        self, response: JSONResponse, access_token: str, refresh_token: str
    ) -> JSONResponse:
        """
        쿠키에 Access, Refresh Token을 부착하는 메소드

        Args:
            response (JSONResponse): 쿠키 생성해줄 response 객체
            access_token (str): Access Token JWT
            refresh_token (str): Refresh Token JWT
        Returns:
            JSONResponse: 쿠키가 부착된 JSONResponse 객체
        """
        response.set_cookie(
            key="access",
            samesite="None",
            secure=True,
            httponly=True,
            value=access_token,
        )
        response.set_cookie(
            key="refresh",
            samesite="None",
            httponly=True,
            secure=True,
            value=refresh_token,
        )
        return response

    async def delete_token_from_cookie(self, response: JSONResponse) -> JSONResponse:
        """
        쿠키의 max_age를 0으로 설정해 쿠키를 지워준다.
        Args:
            response (JSONResponse): 쿠키를 제거할 response 객체
        Returns:
            JSONResponse: 쿠키가 제거된 response 객체
        """
        response.set_cookie(
            key="access",
            samesite="None",
            secure=True,
            httponly=True,
            value="",
            max_age=0,
        )
        response.set_cookie(
            key="refresh",
            samesite="None",
            httponly=True,
            secure=True,
            value="",
            max_age=0,
        )
        return response
