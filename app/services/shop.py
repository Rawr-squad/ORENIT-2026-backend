from fastapi import HTTPException
from app.models.models import User, Currency, NicknameColor, UserStatus


class ShopService:

    def __init__(self, db):
        self.db = db

    def buy_color(self, user_id: int, color_id: int):
        user = self.db.get(User, user_id)
        color = self.db.get(NicknameColor, color_id)

        if not color:
            raise HTTPException(404, "Color not found")

        currency = self._get_currency(user_id)

        if currency.coins < color.price:
            raise HTTPException(400, "Not enough coins")

        if user.nickname_color == color.hex_code:
            raise HTTPException(400, "Color already applied")

        currency.coins -= color.price
        user.nickname_color = color.hex_code

        self.db.commit()

        return {
            "message": "Color purchased",
            "color": color.hex_code,
            "coins_left": currency.coins
        }

    def buy_status(self, user_id: int, status_id: int):
        user = self.db.get(User, user_id)
        status = self.db.get(UserStatus, status_id)

        if not status:
            raise HTTPException(404, "Status not found")

        currency = self._get_currency(user_id)

        if currency.coins < status.price:
            raise HTTPException(400, "Not enough coins")

        if user.status_title == status.title:
            raise HTTPException(400, "Status already active")

        currency.coins -= status.price
        user.status_title = status.title

        self.db.commit()

        return {
            "message": "Status purchased",
            "status": status.title,
            "coins_left": currency.coins
        }

    def _get_currency(self, user_id):
        currency = self.db.get(Currency, user_id)

        if not currency:
            raise HTTPException(400, "User has no balance")

        return currency