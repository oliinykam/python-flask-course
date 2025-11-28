from . import post_bp
from flask import render_template, redirect, url_for, flash, abort, request, session
from app import db 
from .models import Post, PostCategory, User, Tag 
from .forms import PostForm 
from sqlalchemy import select 

@post_bp.route('/<int:id>') 
def detail_post(id):
    """
    Відображає деталі одного поста. Оновлено для eager loading зв'язків User та Tag.
    """
    post = db.session.scalar(
        select(Post).filter_by(id=id).options(db.selectinload(Post.tags), db.joinedload(Post.user))
    )
    
    if post is None or not post.is_active:
        abort(404)
        
    return render_template("detail_post.html", post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
        
    if form.validate_on_submit():
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.posted.data,
            is_active=form.is_active.data,
            category=PostCategory(form.category.data), 
            user_id=form.author_id.data,
            tags=selected_tags 
        )
        db.session.add(new_post)
        db.session.commit()
        
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.detail_post', id=new_post.id))
    
    return render_template(
        "add_post.html", form=form, form_title="Створення нового поста"
    )

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.session.scalar(
        select(Post).filter_by(id=id).options(db.selectinload(Post.tags), db.joinedload(Post.user))
    )
    
    if post is None:
        abort(404)
        
    form = PostForm(obj=post) 
    form.submit.label.text = "Оновити пост"
    
    if request.method == 'GET':
        form.author_id.data = post.user_id 
        form.tags.data = [tag.id for tag in post.tags] 
    
    if form.validate_on_submit():
        selected_tags = db.session.scalars(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).all()
        
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.is_active = form.is_active.data
        post.category = PostCategory(form.category.data) 
        post.user_id = form.author_id.data 
        post.tags = selected_tags 
        
        db.session.commit()
        
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template(
        "add_post.html", form=form, form_title="Редагування поста"
    )

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    """
    Обробляє видалення поста.
    """
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Пост успішно видалено.', 'success')
        return redirect(url_for('posts.get_posts'))

    return render_template("delete_confirm.html", post=post)

@post_bp.route('/') 
def get_posts():
    """
    Відображає список лише АКТИВНИХ постів.
    """
    posts = db.session.scalars(
        db.select(Post).join(Post.user).where(Post.is_active == True).order_by(Post.posted.desc()) 
    ).all()
    
    return render_template("posts.html", posts=posts)