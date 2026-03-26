from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Module
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.module import ModuleCreate

router = APIRouter(prefix="/admin/modules")


@router.post("")
def create_module(
    data: ModuleCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    module = Module(**data.model_dump())
    db.add(module)
    db.commit()
    return module