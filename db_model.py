from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

class Trail(Base):
    __tablename__ = 'trails'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True, unique=True)
    events = relationship('Event', backref='trail', lazy='dynamic')

    def __repr__(self):
        return '<Trail %r>' % (self.name)


class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    status = Column(String(25))
    timestamp = Column(DateTime)
    trail_id = Column(Integer, ForeignKey('trails.id'))

    def __repr__(self):
        return '<Event %r>' % (self.status)