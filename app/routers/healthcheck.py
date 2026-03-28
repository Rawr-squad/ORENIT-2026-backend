from fastapi import Depends, APIRouter
from sqlalchemy import text
from sqlalchemy.orm.session import Session

from app.core.db import get_db

router = APIRouter(prefix='/health')

@router.get("")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        print(f"Health check failed: {e}")
        return {"status": "error", "detail": str(e)}