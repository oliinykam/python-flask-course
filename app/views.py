from app import app
from flask import render_template

@app.route('/')
@app.route('/resume')
def resume():
    page_title = "Моє Резюме"
    return render_template('resume.html', title=page_title)

@app.route('/contacts')
def contacts():
    page_title = "Контакти"
    return render_template('contacts.html', title=page_title)

