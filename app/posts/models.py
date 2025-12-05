import enum
from datetime import datetime
from app import db, login_manager 
from flask_login import UserMixin

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    String, 
    Text, 
    Integer, 
    Boolean, 
    DateTime, 
    Enum, 
    ForeignKey,
    Table,
    Column
)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class PostCategory(enum.Enum):
    NEWS = 'news'
    PUBLICATION = 'publication'
    TECH = 'tech'
    OTHER = 'other'

    def __str__(self):
        return self.value

class User(db.Model, UserMixin): 
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False) 
    
    posts: Mapped[list["Post"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

post_tags = Table(
    'post_tags',
    db.Model.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(db.Model):
    __tablename__ = 'tags'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")
    
    def __repr__(self):
        return f"Tag(id={self.id}, name='{self.name}')"

class Post(db.Model):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(Enum(PostCategory), default=PostCategory.OTHER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}')"