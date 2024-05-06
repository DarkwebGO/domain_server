from flask_sqlalchemy import SQLAlchemy
from .database import db  # 변경된 임포트 경로

class Darkweb(db.Model):
    __tablename__ = 'darkweb'

    id = db.Column(db.Integer, primary_key=True)
    conductor = db.Column(db.String(10), nullable=False)
    domain = db.Column(db.String(100), nullable=False)

class DomainToURL(db.Model):
    __tablename__ = 'domain_to_url'

    id = db.Column(db.Integer, primary_key=True)
    darkweb_id = db.Column(db.Integer, db.ForeignKey('darkweb.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    parameter = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=True)
    keyword = db.Column(db.String(5000), nullable=True)
    html_content = db.Column(db.String(100), nullable=True)

    darkweb = db.relationship('Darkweb', backref=db.backref('urls', lazy=True))

class UrlWeb(db.Model):
    __tablename__ = 'url_web'

    id = db.Column(db.Integer,primary_key=True)
    domain = db.Column(db.String(100),nullable=False)
    last_mdate = db.Column(db.String(10),nullable=True)
    status = db.Column(db.String(8),nullable=False)