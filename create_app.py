import os
from flask import Flask
from flask_migrate import Migrate
from models import db
from auth.routes import auth_blueprint
from blog.routes import blog_blueprint
from profile.routes import profile_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder do przechowywania przesłanych plików
    
    db.init_app(app)
    migrate = Migrate(app, db)
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(blog_blueprint, url_prefix='/blog')
    app.register_blueprint(profile_blueprint, url_prefix='/profile')
    
    return app
