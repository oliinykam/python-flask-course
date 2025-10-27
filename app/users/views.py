from flask import Blueprint, render_template, redirect, url_for, request, flash, session

users_bp = Blueprint(
    'users_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@users_bp.route("/hi/<string:name>") #/hi/ivan?age=45
def greetings (name):
    name = name.upper()
    age = request.args.get("age", None, int)
    return render_template("users/hi.html",name=name, age=age, title="Greating Page")

@users_bp.route("/admin")
def admin():
    to_url = url_for("users_bp.greetings", name="administrator", age=45, _external=True,title="Greating Page")
    print(to_url)
    return redirect(to_url)

VALID_CREDENTIALS = {
    'admin': 'password123',
    'user1': 'mypass456'
}

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in VALID_CREDENTIALS and VALID_CREDENTIALS[username] == password:
            session['username'] = username
            flash('Ви успішно увійшли в систему!', 'success')
            return redirect(url_for('users_bp.profile'))
        else:
            flash('Невірне ім\'я користувача або пароль!', 'error')
            return redirect(url_for('users_bp.login'))
    
    return render_template('users/login.html')

@users_bp.route("/profile")
def profile():
    if 'username' not in session:
        flash('Будь ласка, увійдіть в систему для доступу до профілю!', 'warning')
        return redirect(url_for('users_bp.login'))
    
    username = session['username']
    return render_template('users/profile.html', username=username)

@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    flash('Ви успішно вийшли з системи!', 'info')
    return redirect(url_for('users_bp.login'))
