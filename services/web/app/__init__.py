from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import db  # 변경된 임포트 경로
from .models import Darkweb, DomainToURL, UrlWeb  # 모든 모델을 먼저 임포트


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # app 객체에 db를 초기화

    with app.app_context():
        db.create_all()

    from .commands import setup_app_commands

    from .views import main as main_blueprint

    app.register_blueprint(main_blueprint)
    setup_app_commands(app, db)
    
    return app