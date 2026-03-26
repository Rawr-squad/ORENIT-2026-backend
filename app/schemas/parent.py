from pydantic import BaseModel

class ParentLinkRequest(BaseModel):
    parent_email: str