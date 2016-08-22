# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    def __repr__(self):
        return '<Entry(name="%s">' % self.name

if __name__ == '__main__':
    # initialize the DB
    Base.metadata.create_all(engine)
