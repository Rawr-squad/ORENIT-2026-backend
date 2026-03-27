from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Module, Achievement, NicknameColor, UserStatus
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.module import ModuleCreate

router = APIRouter(prefix="/admin/shop")


@router.post("/colors")
def create_color(name: str, hex_code: str, price: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):

    exists = db.query(NicknameColor).filter(
        (NicknameColor.name == name) |
        (NicknameColor.hex_code == hex_code)
    ).first()

    if exists:
        raise HTTPException(400, "Color already exists")

    color = NicknameColor(
        name=name,
        hex_code=hex_code,
        price=price
    )

    db.add(color)
    db.commit()
    return color

@router.post("/admin/statuses")
def create_status(title: str, price: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):

    exists = db.query(UserStatus).filter_by(title=title).first()
    if exists:
        raise HTTPException(400, "Status exists")

    status = UserStatus(title=title, price=price)

    db.add(status)
    db.commit()
    return status
