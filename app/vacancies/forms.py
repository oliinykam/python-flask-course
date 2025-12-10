from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from app import db
from .models import Category

class VacancyForm(FlaskForm):
    title = StringField('Назва вакансії', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(max=100, message="Назва занадто довга")
    ])
    
    company = StringField('Компанія', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(max=100)
    ])
    
    salary = StringField('Зарплата', validators=[
        Length(max=50)
    ])
    
    description = TextAreaField('Опис вакансії', validators=[
        DataRequired(message="Опис не може бути пустим")
    ])
    
    category_id = SelectField('Категорія', coerce=int, validators=[
        DataRequired(message="Будь ласка, оберіть категорію")
    ])
    
    submit = SubmitField('Зберегти')

    def __init__(self, *args, **kwargs):
        super(VacancyForm, self).__init__(*args, **kwargs)
        try:
            self.category_id.choices = [(c.id, c.name) for c in db.session.query(Category).all()]
        except Exception:
            self.category_id.choices = []

class SearchForm(FlaskForm):
    query = StringField('Пошук', validators=[])
    submit = SubmitField('Знайти')  