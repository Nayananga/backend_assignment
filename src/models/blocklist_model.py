from src.db import db


class BlockListModel(db.Model):
    __tablename__ = "blocklist"

    jti_blocklist = db.Column(db.String(), primary_key=True)
