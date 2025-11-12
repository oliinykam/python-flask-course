from . import post_bp
from flask import render_template, redirect, url_for, flash, abort, request, session
from app import db 
from .models import Post, PostCategory 
from .forms import PostForm 

@post_bp.route('/') 
def get_posts():
    """
    Відображає список лише АКТИВНИХ постів,
    сортуючи їх за датою (новіші зверху).
    """
    posts = db.session.scalars(
        db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    ).all()
    
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    """
    Відображає деталі одного поста.
    Якщо пост неактивний, показує 404.
    """
    post = db.get_or_404(Post, id)
    
    if not post.is_active:
        abort(404)
        
    return render_template("detail_post.html", post=post)

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    
    if 'username' in session:
        form.author.data = session['username']
        form.author.render_kw = {'readonly': True}
        
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            posted=form.posted.data,
            is_active=form.is_active.data,
            category=PostCategory(form.category.data), 
            author=form.author.data 
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
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post) 
    
    form.submit.label.text = "Оновити пост"
    if 'username' in session:
        form.author.data = session.get('username', post.author) 
        form.author.render_kw = {'readonly': True}
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.posted = form.posted.data
        post.is_active = form.is_active.data
        post.category = PostCategory(form.category.data) 
        post.author = form.author.data
        
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