from pydantic import BaseModel

class BlogRequest(BaseModel):
    topic: str
    user_details: str
