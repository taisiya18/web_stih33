import sqlalchemy
from data.db_session import SqlAlchemyBase


class PoemTags(SqlAlchemyBase):
    __tablename__ = 'poem_tags'
    poem_id = sqlalchemy.Column(sqlalchemy.ForeignKey('poems.id'), primary_key=True, nullable=False)
    tag = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True, nullable=False)
