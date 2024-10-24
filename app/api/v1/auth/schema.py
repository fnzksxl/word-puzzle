from pydantic import BaseModel


class GeneralAuthModel(BaseModel):
    email: str
    password: str
    nickname: str
