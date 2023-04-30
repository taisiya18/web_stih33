import sqlalchemy
from data.db_session import SqlAlchemyBase


class Tags(SqlAlchemyBase):
    __tablename__ = 'tags'
    tag = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True, unique=True, nullable=False)
