from typing import List
from pydantic import BaseModel


class ChatResponse(BaseModel):
    action: str
    answer: str


class Question(BaseModel):
    question: str
    options: List[str]
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    action: str
    title: str
    instructions: str
    questions: List[Question]


class ActivityResponse(BaseModel):
    action: str
    title: str
    objective: str
    instructions: List[str]
    estimated_time_minutes: int
    expected_result: str


class ErrorResponse(BaseModel):
    status: str
    code: str
    message: str
