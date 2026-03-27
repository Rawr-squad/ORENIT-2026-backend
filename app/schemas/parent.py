from pydantic import BaseModel, EmailStr


class ParentLinkRequest(BaseModel):
    parent_email: EmailStr