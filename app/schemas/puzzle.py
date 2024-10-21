from pydantic import BaseModel, conint
from typing import Optional


class PuzzleSize(BaseModel):
    size: Optional[conint(ge=7, le=10)] = None
