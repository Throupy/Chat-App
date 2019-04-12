"""SQLAlchemy models."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Message(Base):
    """Message object."""

    __tablename__ = 'message'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    author = Column(String(40), nullable=False)

    def row2dict(row):
        """Row to dict."""
        d = {}
        for column in row.__table__.columns:
            d[column.name] = str(getattr(row, column.name))
        return d


engine = create_engine('sqlite:///chat_app.db')
Base.metadata.create_all(engine)
