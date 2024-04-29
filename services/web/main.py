from flask import Flask, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 현재 파일의 위치 (main.py)
current_path = os.path.dirname(os.path.abspath(__file__))
# 상대 경로를 사용하여 insuck 디렉토리 위치를 계산
json_directory = os.path.join(current_path, '..', '..', 'function', 'insuck')

class Darkweb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    parameter = db.Column(db.String(200), nullable=True)  # 파라미터는 선택적이라 가정
    title = db.Column(db.String(200), nullable=False)
    words = db.Column(db.String(5000),nullable=False)
    html_content = db.Column(db.String(100),nullable=True) #우선적으로 


def print_all_entries():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = Darkweb.query.all()
    for entry in all_entries:
        print(f"ID: {entry.id}, Domain: {entry.domain}, URL: {entry.url}, Depth: {entry.depth}, Parameter: {entry.parameter}, Title: {entry.title}, Words: {entry.words}")


def init_db():
    db.drop_all()  # 기존 데이터베이스의 모든 테이블 삭제, 다시 재구성할때만 실행
    db.create_all()
    import_excel_to_db()  # Excel 데이터 가져오기 실행
    # print_all_entries()  # 데이터베이스에 저장된 모든 데이터 출력

app.before_request(init_db)

def import_excel_to_db():
    base_directory = os.path.join(os.path.dirname(__file__), '..', 'function')
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.xlsx'):
                excel_path = os.path.join(root, file)
                df = pd.read_excel(excel_path)
                for _, row in df.iterrows():
                    html_here = row['URL'].replace('http://', '').replace('/', '_')
                    darkweb_entry = Darkweb(
                        domain=row['Domain'],
                        url=row['URL'],
                        depth=row['Depth'],
                        parameter=row.get('Parameter'),
                        title=row['Title'],
                        words=row['Words'],
                        html_content=html_here
                    )
                    db.session.add(darkweb_entry)
                db.session.commit()

@app.route('/')
def home():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = Darkweb.query.all()
    return render_template('index.html', entries=all_entries)

@app.route('/<html_content>')
def crawl_html(html_content):
    # 서비스 기능 폴더 경로
    base_directory = os.path.join(os.path.dirname(__file__), '..', 'function')
    
    # 요청된 HTML 파일을 찾기 위해 서비스 기능 폴더 안의 모든 폴더를 검색
    for root, dirs, files in os.walk(base_directory):
        for subdir in dirs:
            html_file_path = os.path.join(root, subdir, f'{html_content}.html')
            if os.path.exists(html_file_path):
                print("hihi")
                return send_from_directory(os.path.join(base_directory, subdir), f'{html_content}.html')
    
    # 해당하는 HTML 파일을 찾지 못한 경우 404 에러 반환
    return 'Not Found', 404

if __name__ == '__main__':
    ## 저장된 json 불러오는 코드 작성하기... 
    app.run(debug=True)
