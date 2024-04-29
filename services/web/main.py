from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Darkweb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

@app.before_request
def init_db():
    db.create_all()
    print("Database initialized successfully!")

@app.route('/')
def home():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = Darkweb.query.all()
    return render_template('index.html', entries=all_entries)

if __name__ == '__main__':
    app.run(debug=True)
