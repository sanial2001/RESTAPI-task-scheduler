from .db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_head = Column(Boolean, default=False)
    club = relationship('Club', back_populates='user')


class Club(Base):
    CLUBS_REGISTERED = (
        ('IIITG', 'iiitg'),
        ('PROGRAMMING', 'programming'),
        ('ROBOTICS', 'robotics'),
        ('DANCE', 'dance'),
        ('MUSIC', 'music'),
        ('ARTS', 'arts'),
        ('SPORTS', 'sports'),
        ('QUIZ', 'quiz'),
        ('READING', 'reading'),
        ('PORTRAITURE', 'portraiture'),
        ('DRAMA', 'drama'),
    )

    __tablename__ = "clubs"
    id = Column(Integer, primary_key=True, nullable=False)
    clubs_registered = Column(ChoiceType(choices=CLUBS_REGISTERED), default="IIITG")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship('User', back_populates='club')
