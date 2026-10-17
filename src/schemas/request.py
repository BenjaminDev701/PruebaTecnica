from pydantic import BaseModel


class ExecuteRequest(BaseModel):
    action: str
    book_id: str
    section_id: str
    instructions: str
