import sqlalchemy
from data.db_session import SqlAlchemyBase
from datetime import datetime


class Poems(SqlAlchemyBase):
    __tablename__ = 'poems'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'), nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    content = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_on = sqlalchemy.Column(sqlalchemy.DateTime(), default=datetime.now, nullable=False)
