from flask import Blueprint, render_template, redirect, url_for, request, flash

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

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'username' or \
                request.form['password'] != 'password':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return redirect(url_for('users_bp.profile'))
    return render_template("users/login.html",title="Login Page", error=error)

@users_bp.route("/profile")
def profile():
    return render_template("users/profile.html",title="Profile page")

