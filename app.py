from flask import Flask, render_template
from create_app import create_app
from models import db
from flask_migrate import Migrate
from flask_login import current_user, LoginManager

app = create_app()
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')


@app.context_processor
def inject_current_user():
    return dict(current_user=current_user)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
