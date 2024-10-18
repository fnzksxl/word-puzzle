from pydantic import BaseModel, conint


class PuzzleSize(BaseModel):
    size: conint(ge=7, le=10)
