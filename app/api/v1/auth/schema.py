from pydantic import BaseModel


class GeneralLoginModel(BaseModel):
    email: str
    password: str


class GeneralRegisterModel(GeneralLoginModel):
    nickname: str
