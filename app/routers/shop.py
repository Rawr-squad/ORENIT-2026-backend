from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.models import NicknameColor, UserStatus
from app.services.shop import ShopService

router = APIRouter(prefix="/shop", tags=["shop"])


@router.get("/colors")
def get_colors(db: Session = Depends(get_db)):
    from app.models.models import NicknameColor
    return db.query(NicknameColor).all()


@router.get("/statuses")
def get_statuses(db: Session = Depends(get_db)):
    from app.models.models import UserStatus
    return db.query(UserStatus).all()


@router.post("/buy/color/{color_id}")
def buy_color(color_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    return ShopService(db).buy_color(user.id, color_id)


@router.post("/buy/status/{status_id}")
def buy_status(status_id: int, user=Depends(get_current_user), db=Depends(get_db)):
    return ShopService(db).buy_status(user.id, status_id)

@router.post('/seed')
def create_shop_items(db : Session = Depends(get_db)):
    colors = [
        ("Red", "#FF0000", 3),
        ("Green", "#00FF00", 3),
        ("Blue", "#0000FF", 3),
    ]

    statuses = [
        ("Знаток", 2),
        ("Мастер", 3),
        ("Гуру", 5),
    ]

    for name, hex_code, price in colors:
        db.add(NicknameColor(name=name, hex_code=hex_code, price=price))

    for title, price in statuses:
        db.add(UserStatus(title=title, price=price))

    db.commit()
