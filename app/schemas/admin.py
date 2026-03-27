from pydantic import BaseModel


class ReviewAttemptRequest(BaseModel):
    is_correct: bool