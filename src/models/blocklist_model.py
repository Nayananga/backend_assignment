from sqlalchemy import Column, String

from src.db import db


class BlockListModel(db.Model):
    __tablename__ = "blocklist"

    jti_blocklist = Column(String, primary_key=True)
