from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Attempt, Currency
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.admin import ReviewAttemptRequest

router = APIRouter(prefix="/admin/attempts")


@router.get("/pending")
def get_pending(db: Session = Depends(get_db), admin=Depends(require_role(["admin"]))):
    return db.query(Attempt).filter_by(status="pending").all()


@router.post("/{id}/review")
def review(
    id: int,
    data: ReviewAttemptRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    attempt = db.get(Attempt, id)

    attempt.is_correct = data.is_correct
    attempt.status = "checked"
    attempt.reviewer_id = admin.id

    if data.is_correct:
        cur = db.get(Currency, attempt.user_id)
        if not cur:
            cur = Currency(user_id=attempt.user_id, xp=0)
            db.add(cur)
        cur.xp += 20

    db.commit()
    return attempt