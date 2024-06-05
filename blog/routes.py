from flask import Blueprint, render_template, redirect, url_for, request, flash, session,g
from werkzeug.utils import secure_filename
from models import db, BlogPost, User
import os

blog_blueprint = Blueprint('blog', __name__)



@blog_blueprint.route('/')
def index():
    _zmienna = 'dodano post'
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog_index.html', posts=posts)

@blog_blueprint.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    author = User.query.get(post.author_id)
    return render_template('blog_post.html', post=post, author=author)

@blog_blueprint.route('/post/new', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = session.get('user_id')
        if not author_id:
            flash('You need to log in first.', 'danger')
            return redirect(url_for('auth.login'))
        post = BlogPost(title=title, content=content, author_id=author_id)
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join('static/uploads', filename))
                post.image = 'uploads/' + filename
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully.', 'success')
        return redirect(url_for('blog.index'))
    return render_template('create_post.html')

@blog_blueprint.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        #post.author = User.query.get(post.author_id)
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join('static/uploads', filename))
                post.image = 'uploads/' + filename
        db.session.commit()
        flash('Post updated successfully.', 'success')
        return redirect(url_for('blog.post', post_id=post.id))
    return render_template('edit_post.html', post=post)
