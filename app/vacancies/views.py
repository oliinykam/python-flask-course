from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from . import vacancies_bp
from .models import Vacancy, Category
from .forms import VacancyForm, SearchForm

@vacancies_bp.route('/', methods=['GET'])
def list_vacancies():
    search_form = SearchForm(request.args)
    
    query = Vacancy.query

    if search_form.query.data:
        search_term = f"%{search_form.query.data}%"
        query = query.filter(Vacancy.title.like(search_term) | Vacancy.company.like(search_term))

    sort_by = request.args.get('sort', 'date')
    if sort_by == 'salary':
        query = query.order_by(Vacancy.salary.desc())
    else:
        query = query.order_by(Vacancy.created_at.desc())

    vacancies = query.all()
    
    return render_template('vacancies/list.html', vacancies=vacancies, form=search_form)

@vacancies_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = VacancyForm()

    if form.validate_on_submit():
        vacancy = Vacancy(
            title=form.title.data,
            company=form.company.data,
            salary=form.salary.data or "Не вказано", 
            description=form.description.data,
            category_id=form.category_id.data,
            user=current_user
        )
        db.session.add(vacancy)
        db.session.commit()
        flash('Вакансію успішно створено!', 'success')
        return redirect(url_for('vacancies.list_vacancies'))
    
    return render_template('vacancies/form.html', form=form, title="Створити вакансію")

@vacancies_bp.route('/<int:id>')
def detail(id):
    vacancy = db.get_or_404(Vacancy, id)
    return render_template('vacancies/detail.html', vacancy=vacancy)

@vacancies_bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    vacancy = db.get_or_404(Vacancy, id)
    
    if vacancy.user != current_user:
        abort(403)

    form = VacancyForm(obj=vacancy)
    if form.validate_on_submit():
        vacancy.title = form.title.data
        vacancy.company = form.company.data
        vacancy.salary = form.salary.data or "Не вказано"
        vacancy.description = form.description.data
        vacancy.category_id = form.category_id.data
        
        db.session.commit()
        flash('Вакансію оновлено!', 'success')
        return redirect(url_for('vacancies.detail', id=vacancy.id))
        
    return render_template('vacancies/form.html', form=form, title="Редагувати вакансію")

@vacancies_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    vacancy = db.get_or_404(Vacancy, id)
    
    if vacancy.user != current_user:
        abort(403)
        
    db.session.delete(vacancy)
    db.session.commit()
    flash('Вакансію видалено.', 'info')
    return redirect(url_for('vacancies.list_vacancies'))