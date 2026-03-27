from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.models import User, ParentChild
from app.schemas.parent import ParentLinkRequest

router = APIRouter()


@router.post("/parent-link")
def link(
    data: ParentLinkRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    parent = db.query(User).filter_by(
        email=data.parent_email,
        role="parent"
    ).first()

    existing = db.query(ParentChild).filter_by(
        parent_id=parent.id,
        child_id=user.id
    ).first()

    if existing:
        raise HTTPException(400, "Already linked")

    rel = ParentChild(parent_id=parent.id, child_id=user.id)
    db.add(rel)
    db.commit()

    return {"ok": True}