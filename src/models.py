from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_planets = Table(
    'user_planets',
    db.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('planet_id', Integer, ForeignKey('planet.id'), primary_key=True)
)

user_characters = Table(
    'user_characters',
    db.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('character_id', Integer, ForeignKey('character.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

favorite_planets: Mapped[list['Planet']] = relationship(
    'Planet',
    secondary=user_planets,
    back_populates='favorited_by'
)

favorite_character: Mapped[list['Character']] = relationship(
    'Character',
    secondary=user_characters,
    back_populates='favorited_by'
)

posts: Mapped[list['Post']] = relationship('post', back_populates='author')
comments: Mapped[list['Comment']] = relationship('Comment', back_populates='author')

def serialize(self):
    return {
        "id": self.id,
        "email": self.email,
            # do not serialize the password, its a security breach
    }

class Planet(db.Model):
    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    climate: Mapped[str] = mapped_column(String(80))
    population: Mapped[int] = mapped_column(Integer)

    favorite_by: Mapped[list['User']] = relationship(
        'User',
        secondary=user_planets,
        back_populates='favorite_planets'
    )

class Character(db.Model):
    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    species: Mapped[str] = mapped_column(String(80))
    gender: Mapped[str] = mapped_column(String(80))

    favorite_by: Mapped[list['User']] = relationship(
        'User',
        secondary=user_characters,
        back_populates='favorite_characters'
    )

class Post(db.Model):
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    msg: Mapped[str] = mapped_column(Text, nullable=False)
    
    comments: Mapped[list['Comment']] = relationship('Comment', back_populates='post')
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey('user.id'), nullable=False)
    author: Mapped['User'] = relationship('User', back_populates='post')

    
class Comment(db.Model):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    
    
    post: Mapped[list['Post']] = relationship('Post', back_populates='comment')
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey('post.id'), nullable=False)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey('user.id'), nullable=False)
    author: Mapped['User'] = relationship('User', back_populates='post')
