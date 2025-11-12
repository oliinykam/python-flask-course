from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from .config import config 
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
import os

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name: str = os.environ.get("FLASK_CONFIG", "dev")) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    print(f"Running in config: {config_name}")

    db.init_app(app)
    migrate.init_app(app, db)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    with app.app_context():
        from . import views as main_blueprint
        app.register_blueprint(main_blueprint.main_bp)
        
        from .users.views import users_bp
        app.register_blueprint(users_bp)
        
        from .posts import post_bp
        app.register_blueprint(post_bp)
        
        from .posts import models 

    return app