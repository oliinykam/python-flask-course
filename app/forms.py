from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TelField, SelectField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, Regexp

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
    """
    Клас форми для входу користувача.
    """
    
    username = StringField("Ім'я користувача", validators=[
        DataRequired(message="Це поле обов'язкове") 
    ])
    
    password = PasswordField('Пароль', validators=[
        DataRequired(message="Це поле обов'язкове"),
        Length(min=4, max=10, message='Пароль має бути від 4 до 10 символів') 
    ])
    
    remember = BooleanField("Запам'ятати мене")
    
    submit = SubmitField('Увійти') 