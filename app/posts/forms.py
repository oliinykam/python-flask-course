from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField,
    SelectMultipleField, 
    BooleanField,
    DateTimeLocalField  
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from datetime import datetime
from app import db 
from .models import PostCategory, User, Tag 

class PostForm(FlaskForm):
    """
    Форма для створення/редагування поста.
    """
    
    title = StringField(
        "Заголовок", 
        validators=[DataRequired(), Length(max=150)]
    )
    
    content = TextAreaField(
        "Вміст", 
        validators=[DataRequired()]
    )
    
    author_id = SelectField(
        "Автор", 
        coerce=int, 
        validators=[DataRequired()]
    )
    
    is_active = BooleanField(
        "Активний (відображається на сайті)", 
        default=True      
    )
    
    posted = DateTimeLocalField(
        "Дата публікації",
        format='%Y-%m-%dT%H:%M',
        default=datetime.utcnow,
        validators=[DataRequired()]
    )
    
    category = SelectField(
        "Категорія",
        choices=[(cat.value, cat.name.capitalize()) for cat in PostCategory],
        validators=[DataRequired()]
    )

    tags = SelectMultipleField(
        "Теги",
        coerce=int,
        validators=[]
    )
    
    submit = SubmitField("Створити пост")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        authors = db.session.scalars(db.select(User).order_by(User.id)).all()
        self.author_id.choices = [(a.id, a.username) for a in authors]
        
        tags_list = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()
        self.tags.choices = [(t.id, t.name) for t in tags_list]