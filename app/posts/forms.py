from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    TextAreaField, 
    SubmitField, 
    SelectField,
    BooleanField,
    DateTimeLocalField  
)
from wtforms.validators import (
    DataRequired, 
    Length
)
from datetime import datetime
from .models import PostCategory  

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
    
    author = StringField(
        'Автор', 
        validators=[DataRequired(), Length(max=20)], 
        default='Anonymous'
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
    
    submit = SubmitField("Створити пост")