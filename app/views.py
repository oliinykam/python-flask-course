import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import ContactForm  

logging.basicConfig(
    filename='contacts.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/resume')
def resume():
    page_title = "Моє Резюме"
    return render_template('resume.html', title=page_title)

@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data

        try:
            logging.info(
                f"New Contact Form Submission: "
                f"Name='{name}', Email='{email}', "
                f"Subject='{dict(form.subject.choices).get(subject)}', Message='{message}'"
            )
            flash(f'Дякуємо, {name}! Ваше повідомлення ({email}) було успішно надіслано.', 'success')
        except Exception as e:
            logging.error(f"Failed to log contact submission: {e}")
            flash('Сталася помилка під час збереження вашого повідомлення. Спробуйте пізніше.', 'danger')

        return redirect(url_for('.contacts')) 
    
    elif request.method == 'POST':
        flash('Будь ласка, виправте помилки у формі та спробуйте знову.', 'danger')

    return render_template('contacts.html', form=form)