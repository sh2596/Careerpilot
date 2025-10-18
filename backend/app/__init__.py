# backend/app/__init__.py
from flask import Flask
from config import Config
from app.extensions import db, jwt  # ✅ Import from extensions

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints AFTER db is ready
    from app.routes.auth import auth_bp
    from app.routes.jobs import jobs_bp
    from app.routes.resumes import resumes_bp  # ✅ Safe now

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(jobs_bp, url_prefix='/jobs')
    app.register_blueprint(resumes_bp, url_prefix='/resumes')

    with app.app_context():
        db.create_all()

    return app