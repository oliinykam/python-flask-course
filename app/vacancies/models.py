from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer, ForeignKey, DateTime
from app import db

from app.posts.models import User 

class Category(db.Model):
    __tablename__ = 'vacancies_categories'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    
    vacancies: Mapped[list["Vacancy"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"Category('{self.name}')"

class Vacancy(db.Model):
    __tablename__ = 'vacancies'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str] = mapped_column(String(100), nullable=False)
    salary: Mapped[str] = mapped_column(String(50), nullable=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    category_id: Mapped[int] = mapped_column(ForeignKey('vacancies_categories.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    
    category: Mapped["Category"] = relationship(back_populates="vacancies")
    user: Mapped["User"] = relationship(back_populates="vacancies")


    def __repr__(self):
        return f"Vacancy('{self.title}', '{self.company}')"