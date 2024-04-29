from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Darkweb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    parameter = db.Column(db.String(200), nullable=True)  # 파라미터는 선택적이라 가정
    title = db.Column(db.String(200), nullable=False)
    words = db.Column(db.String(1000), nullable=False)  # 저장된 단어 목록
    html_content_path = db.Column(db.String(200), nullable=True)  # HTML 파일의 저장 경로

@app.before_request
def init_db():
    ## db.drop_all()  # 기존 데이터베이스의 모든 테이블 삭제, 다시 재구성할때만 실행
    db.create_all()
    print("Database initialized successfully!")

@app.route('/')
def home():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = Darkweb.query.all()
    return render_template('index.html', entries=all_entries)

if __name__ == '__main__':
    app.run(debug=True)
