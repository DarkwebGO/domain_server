from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


role = {
    "insuck" : "인석",
    "minsu" : "민수",
    "seohyun" : "서현",
    "yubin" : "유빈"
}

# 현재 파일의 위치 (main.py)
current_path = os.path.dirname(os.path.abspath(__file__))
# 상대 경로를 사용하여 insuck 디렉토리 위치를 계산
json_directory = os.path.join(current_path, '..', '..', 'function', 'insuck')

class Darkweb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conductor = db.Column(db.String(10), nullable=False)
    domain = db.Column(db.String(100), nullable=False)

class DomainToURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    darkweb_id = db.Column(db.Integer, db.ForeignKey('darkweb.id'), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    parameter = db.Column(db.String(200), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    words = db.Column(db.String(5000), nullable=False)
    html_content = db.Column(db.String(100), nullable=True)

    darkweb = db.relationship('Darkweb', backref=db.backref('urls', lazy=True))

class UrlWeb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    domain = db.Column(db.String(100),nullable=False)
    last_mdate = db.Column(db.String(10),nullable=True)
    status = db.Column(db.String(8),nullable=False)


def print_all_entries():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = UrlWeb.query.all()
    for entry in all_entries:
        print(f"ID: {entry.id}, Domain: {entry.domain}")

def init_db():
    db.drop_all()  # 기존 데이터베이스의 모든 테이블 삭제, 다시 재구성할때만 실행
    db.create_all()
    import_excel_to_db()  # Excel 데이터 가져오기 실행
    init_onion()
    init_db_status()
    #print_all_entries()  # 데이터베이스에 저장된 모든 데이터 출력

def init_db_status():
    base_directory = os.path.join(os.path.dirname(__file__), '..', 'function')
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.xlsx'):
                excel_path = os.path.join(root, file)
                df = pd.read_excel(excel_path)
                for _, row in df.iterrows():
                    domain = row['Domain']
                    ## UrlWeb Table에서 해당 domain에 대한 row의 status 값을 True로 설정.
                    UrlWeb.query.filter_by(domain=domain).update({'status': 'true'})
                    db.session.commit()  # 변경 사항을 데이터베이스에 커밋
                
def init_onion():
    # onions.txt 파일 읽기
    try:
        with open('./onions.txt', 'r') as file:
            lines = file.readlines()
        
        # 데이터베이스 세션 시작
        for line in lines:
            domain = line.strip()  # 줄바꿈 제거
            # UrlWeb 인스턴스 생성 및 추가
            url_web = UrlWeb(domain=domain, last_mdate="None", status='false')
            db.session.add(url_web)
        
        # 변경 사항 커밋
        db.session.commit()
    except Exception as e:
        print(f"Error: {e}")


def import_excel_to_db():
    base_directory = os.path.join(os.path.dirname(__file__), '..', 'function')
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.xlsx'):
                file_dir_name = os.path.basename(root)
                file_dir_name = role[file_dir_name]
                excel_path = os.path.join(root, file)
                df = pd.read_excel(excel_path)
                for _, row in df.iterrows():
                    darkweb_entry = Darkweb.query.filter_by(domain=row['Domain']).first()
                    if not darkweb_entry:
                        darkweb_entry = Darkweb(
                            conductor=file_dir_name,
                            domain=row['Domain']
                        )
                        db.session.add(darkweb_entry)
                        db.session.commit()
                    urlweb_entry = DomainToURL(
                        darkweb_id=darkweb_entry.id,
                        url=row['URL'],
                        depth=row['Depth'],
                        parameter=row.get('Parameter'),
                        title=row['Title'],
                        words=row['Words'],
                        html_content=row['URL'].replace('http://', '').replace('/', '_')
                    )
                    db.session.add(urlweb_entry)
                db.session.commit()


@app.route('/')
def home():
    # Darkweb 테이블의 모든 데이터 조회
    all_entries = Darkweb.query.all()
    all_url = DomainToURL.query.all()
    return render_template('index.html', entries=all_entries)

@app.route('/todo')
def todo_onion():
    page_active = int(request.args.get('page_active', 1))
    page_inactive = int(request.args.get('page_inactive', 1))
    items_per_page = 10

    # Active tasks query and pagination
    query_active = UrlWeb.query.filter_by(status='true')
    total_active = query_active.count()
    pagination_active = query_active.paginate(page=page_active, per_page=items_per_page, error_out=False)
    active_list = pagination_active.items
    total_pages_active = pagination_active.pages

    # Inactive tasks query and pagination
    query_inactive = UrlWeb.query.filter_by(status='false')
    total_inactive = query_inactive.count()
    pagination_inactive = query_inactive.paginate(page=page_inactive, per_page=items_per_page, error_out=False)
    inactive_list = pagination_inactive.items
    total_pages_inactive = pagination_inactive.pages

    return render_template('TodoOnion.html', activeList=active_list, numPagesActive=total_pages_active, pageActive=page_active,
                           inactiveList=inactive_list, numPagesInactive=total_pages_inactive, pageInactive=page_inactive,
                           totalActive=total_active, totalInactive=total_inactive)


@app.route('/api')
def false_domain():
    # status가 'false'인 UrlWeb 레코드 랜덤 선택
    url_web = UrlWeb.query.filter_by(status='false').order_by(db.func.random()).first()
    if url_web:
        # 해당 레코드의 status 값을 'true'로 변경
        url_web.status = 'true'
        db.session.commit() 
        return jsonify({'domain': url_web.domain})
    else:
        return jsonify({'error': 'No entries found'}), 404

@app.route('/<html_content>')
def crawl_html(html_content):
    print(html_content)
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
    with app.app_context():
        init_db()
    ## 저장된 json 불러오는 코드 작성하기... 
    app.run(debug=True, host='0.0.0.0')