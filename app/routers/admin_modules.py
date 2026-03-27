from fastapi import APIRouter, Depends, HTTPException
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

@router.put("/{id}")
def update_module(id: int, data: ModuleCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    module = db.get(Module, id)

    if not module:
        raise HTTPException(404, "Module not found")

    module.title = data.title
    module.order = data.order

    db.commit()
    return module


@router.delete("/{id}")
def delete_module(id: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    module = db.get(Module, id)

    if not module:
        raise HTTPException(404, "Module not found")

    db.delete(module)
    db.commit()

    return {"message": "Module deleted"}