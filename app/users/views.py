from flask import Blueprint, render_template, redirect, url_for, request, flash, session, make_response
from flask_login import login_user, current_user, logout_user, login_required
from app import db, bcrypt
from app.posts.models import User
from ..forms import LoginForm, RegistrationForm

users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.account'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Акаунт створено! Тепер ви можете увійти.', 'success')
            return redirect(url_for('users_bp.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Помилка: {str(e)}', 'danger')
            
    return render_template('users/register.html', form=form, title='Реєстрація')

@users_bp.route('/login', methods=['GET', 'POST']) 
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users_bp.account'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.username == form.username.data))
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Вітаємо, {user.username}!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users_bp.account'))
        else:
            flash('Невірні дані для входу.', 'danger')

    return render_template('users/login.html', form=form)

@users_bp.route('/account')
@login_required  
def account():
    return render_template('users/account.html')

@users_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Ви вийшли з системи.', 'info')
    return redirect(url_for('users_bp.login'))

@users_bp.route('/users')
@login_required
def user_list():
    users = db.session.scalars(db.select(User)).all()
    count = len(users)
    return render_template('users/users_list.html', users=users, count=count)

@users_bp.route("/set-theme/<theme_name>")
def set_theme(theme_name):
    session['theme'] = theme_name
    resp = make_response(redirect(url_for('users_bp.profile')))
    resp.set_cookie('theme', theme_name)
    flash(f"Тему змінено на {theme_name}", "info")
    return resp

@users_bp.route('/add-cookie', methods=['POST'])
def add_cookie():
    key = request.form.get('cookie_key')
    value = request.form.get('cookie_value')
    resp = make_response(redirect(url_for('users_bp.profile')))
    if key and value:
        resp.set_cookie(key, value)
        flash(f'Кукі додано', 'success')
    return resp

@users_bp.route('/delete-cookie', methods=['POST'])
def delete_cookie():
    key = request.form.get('cookie_key')
    resp = make_response(redirect(url_for('users_bp.profile')))
    if key:
        resp.delete_cookie(key)
        flash(f'Кукі видалено', 'success')
    return resp

@users_bp.route('/delete-all-cookies', methods=['POST'])
def delete_all_cookies():
    resp = make_response(redirect(url_for('users_bp.profile')))
    for cookie in request.cookies:
        if cookie != 'session':
            resp.delete_cookie(cookie)
    flash('Всі кукі видалено', 'success')
    return resp

@users_bp.route("/admin")
def admin():
    return redirect(url_for("users_bp.greetings", name="Administrator"))

@users_bp.route("/hi/<string:name>")
def greetings(name):
    return render_template("users/hi.html", name=name.upper())