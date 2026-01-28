from pydantic import BaseModel, Field
from typing import Optional


class Note(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    desc: Optional[str] = Field(default="")
    important: bool = False
