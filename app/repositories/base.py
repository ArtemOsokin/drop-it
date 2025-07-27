from sqlalchemy.orm import Session as SessionType


class BaseRepository:
    def __init__(self, db: SessionType):
        self.db = db
