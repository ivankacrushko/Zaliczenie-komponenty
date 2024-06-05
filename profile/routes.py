from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.utils import secure_filename
from models import db, User, BlogPost
import os

profile_blueprint = Blueprint('profile', __name__)

@profile_blueprint.route('/')
def user_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    posts = BlogPost.query.filter_by(author_id=user.id).order_by(BlogPost.created_at.desc()).all()
    return render_template('profile.html', user=user, posts=posts)

@profile_blueprint.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.get(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.country = request.form['country']
        if 'profile_image' in request.files:
            profile_image = request.files['profile_image']
            if profile_image.filename != '':
                filename = secure_filename(profile_image.filename)
                profile_image.save(os.path.join('static/uploads', filename))
                user.profile_image = 'uploads/' + filename
        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.user_profile'))
    return render_template('edit_profile.html', user=user)
