from flask import Flask, g
import sqlite3

# Flask 앱 생성
app = Flask(__name__)

# 데이터베이스 경로 설정
DATABASE = 'database.db'

# 데이터베이스 초기화 함수
def init_db():
    # 데이터베이스 연결
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    # 'darkweb' 테이블 생성
    cur.execute('''
        CREATE TABLE IF NOT EXISTS darkweb (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    
    # 변경 사항 저장
    conn.commit()
    print("Database initialized successfully!")
    conn.close()

# 데이터베이스 연결 함수
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# 앱 종료 시 데이터베이스 연결 해제
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# 라우트 정의
@app.route('/')
def hello_world():
    # 'darkweb' 테이블의 스키마 조회
    conn = get_db()
    cur = conn.cursor() 
    cur.execute("PRAGMA table_info('darkweb')")
    columns = cur.fetchall()
    print("Columns in 'darkweb' table:")
    for column in columns:
        print(column[1], "-", column[2])
    return 'Hello, World!'

# 앱 실행
if __name__ == '__main__':
    init_db()
    app.run(debug=True)
