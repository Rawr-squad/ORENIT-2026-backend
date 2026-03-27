from fastapi import HTTPException
from app.models.models import Comment, Lesson, User


class CommentService:

    def __init__(self, db):
        self.db = db

    def create_comment(self, user, data):
        lesson = self.db.get(Lesson, data.lesson_id)

        if not lesson:
            raise HTTPException(404, "Lesson not found")

        # 🔒 если это reply
        if data.parent_id:
            parent = self.db.get(Comment, data.parent_id)

            if not parent:
                raise HTTPException(404, "Parent comment not found")

            if parent.lesson_id != data.lesson_id:
                raise HTTPException(400, "Invalid parent comment")

        comment = Comment(
            user_id=user.id,
            lesson_id=data.lesson_id,
            parent_id=data.parent_id,
            content=data.content
        )

        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)

        return comment

    def get_comments_tree(self, lesson_id: int):
        comments = self.db.query(Comment).filter_by(
            lesson_id=lesson_id
        ).order_by(Comment.created_at.asc()).all()

        users = {
            u.id: u.nickname
            for u in self.db.query(User).all()
        }

        # 🌳 строим дерево
        tree = {}
        result = []

        for c in comments:
            node = {
                "id": c.id,
                "user_id": c.user_id,
                "nickname": users.get(c.user_id),
                "content": c.content,
                "created_at": c.created_at,
                "replies": []
            }
            tree[c.id] = node

        for c in comments:
            node = tree[c.id]

            if c.parent_id:
                parent = tree.get(c.parent_id)
                if parent:
                    parent["replies"].append(node)
            else:
                result.append(node)

        return result