from typing import Literal
from pydantic import BaseModel


class ExecuteRequest(BaseModel):
    action: Literal["chat", "quiz", "activity"]
    book_id: str
    section_id: str
    instructions: str
