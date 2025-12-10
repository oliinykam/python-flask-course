from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, EmailField, TelField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError

from app import db
from app.posts.models import User

class ContactForm(FlaskForm):
    """Клас контактної форми з валідацією."""
    name = StringField("Ім'я", validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(min=4, max=10, message="Ім'я повинно бути від 4 до 10 символів.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Email(message="Введіть коректний email.")
    ])
    phone = TelField('Телефон', validators=[
        Regexp(r'^\+380\d{9}$', message="Формат телефону має бути +380XXXXXXXXX (9 цифр).")
    ])
    subject = SelectField('Тема', choices=[
        ('general', 'General'),
        ('support', 'Support'),
        ('feedback', 'Feedback'),
        ('other', 'Other')
    ], validators=[DataRequired(message="Будь ласка, оберіть тему.")])
    message = TextAreaField('Повідомлення', validators=[
        DataRequired(message="Це поле обов'язкове."),
        Length(max=500, message="Повідомлення не може перевищувати 500 символів.")
    ])
    submit = SubmitField('Відправити повідомлення')

class LoginForm(FlaskForm):
    """Клас форми для входу користувача."""
    username = StringField("Ім'я користувача", validators=[
        DataRequired(message="Це поле обов'язкове") 
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message='Пароль має бути від 4 до 10 символів') 
    ])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField('Увійти') 

class RegistrationForm(FlaskForm):
    """Форма реєстрації з перевіркою унікальності."""
    username = StringField("Ім'я користувача", validators=[
        DataRequired(),
        Length(min=4, max=20, message="Ім'я має бути від 4 до 20 символів"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
               "Дозволені тільки літери, цифри, крапки та підкреслення")
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(), 
        Email(message="Некоректний email")
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=6, message="Мінімум 6 символів")
    ])
    
    confirm_password = PasswordField('Підтвердження пароля', validators=[
        DataRequired(),
        EqualTo('password', message='Паролі не співпадають')
    ])
    
    submit = SubmitField('Зареєструватися')

    def validate_username(self, field):
        user = db.session.scalar(db.select(User).where(User.username == field.data))
        if user:
            raise ValidationError("Це ім'я вже зайняте.")

    def validate_email(self, field):
        user = db.session.scalar(db.select(User).where(User.email == field.data))
        if user:
            raise ValidationError("Цей email вже використовується.")

class UpdateAccountForm(FlaskForm):
    """Форма оновлення акаунту користувача (Лабораторна 10)."""
    username = StringField("Ім'я користувача", validators=[
        DataRequired(),
        Length(min=4, max=20, message="Ім'я має бути від 4 до 20 символів"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
               "Дозволені тільки літери, цифри, крапки та підкреслення")
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(), 
        Email(message="Некоректний email")
    ])
    
    picture = FileField('Оновити фото профілю', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], message="Дозволені формати: jpg, png, jpeg")
    ])
    
    about_me = TextAreaField('Про мене', validators=[
        Length(max=140, message="Довжина не може перевищувати 140 символів")
    ])
    
    submit_account = SubmitField('Оновити')

    def validate_username(self, field):
        if field.data != current_user.username:
            user = db.session.scalar(db.select(User).where(User.username == field.data))
            if user:
                raise ValidationError("Це ім'я вже зайняте.")

    def validate_email(self, field):
        if field.data != current_user.email:
            user = db.session.scalar(db.select(User).where(User.email == field.data))
            if user:
                raise ValidationError("Цей email вже використовується.")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Поточний пароль', validators=[DataRequired()])
    password = PasswordField('Новий пароль', validators=[
        DataRequired(),
        Length(min=4, max=10, message='Пароль має бути від 4 до 10 символів')
    ])
    confirm_password = PasswordField('Підтвердження пароля', validators=[
        DataRequired(),
        EqualTo('password', message='Паролі не співпадають')
    ])
    submit_password = SubmitField('Змінити пароль')