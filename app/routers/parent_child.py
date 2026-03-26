from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.models import User, ParentChild

router = APIRouter()


@router.post("/parent-link")
def link(parent_email: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    parent = db.query(User).filter_by(email=parent_email, role="parent").first()

    rel = ParentChild(parent_id=parent.id, child_id=user.id)
    db.add(rel)
    db.commit()
    return {"ok": True}