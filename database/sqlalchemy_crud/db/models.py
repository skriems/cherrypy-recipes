import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return '<Entry(name="%s">' % self.name
