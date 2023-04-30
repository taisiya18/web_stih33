import sqlalchemy
from flask_login import UserMixin

from data.db_session import SqlAlchemyBase


class Users(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String(50), nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String(), nullable=False)
