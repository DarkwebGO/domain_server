import os
from flask import current_app
import pandas as pd

# 'db'를 여기서 직접 임포트하지 않고 필요한 곳에서 직접 참조하거나 지역 임포트를 사용합니다.
from .models import Darkweb, DomainToURL, UrlWeb  # 모델 임포트

role = {
    "insuck" : "인석",
    "minsu" : "민수",
    "seohyun" : "서현",
    "yubin" : "유빈"
}

def setup_app_commands(app, db):
    @app.cli.command("init-db") ## db 데이베이스생성.
    def init_db():
        db.drop_all()
        db.create_all()
        print('Initialized the database.')

    @app.cli.command("import-data") ## 데이터 db에 저장
    def import_data():
        """Import data from Excel files and other sources."""
        import_excel_to_db(db)
        print("import_excel_to_db end")
        init_onion(db)
        print("init_onion end")
        init_db_status(db)
        print('Data imported successfully.')



def init_db_status(db):
    base_directory = os.path.join(os.path.dirname(__file__), '..','..', 'function')
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
                
def init_onion(db):
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

def import_excel_to_db(db):
    base_directory = os.path.join(os.path.dirname(__file__), '..', '..', 'function')
    
    for root, dirs, files in os.walk(base_directory):
        # 'function' 바로 아래의 폴더에서 시작
        parts = root.split(os.sep)
        if 'function' in parts:
            # 'function' 바로 다음 폴더의 인덱스를 찾고, 그 폴더 이름을 구합니다
            function_index = parts.index('function')
            if function_index + 1 < len(parts):
                dir_name = parts[function_index + 1]
            else:
                continue  # 'function' 바로 아래 폴더가 아니면 처리하지 않음

            for file in files:
                if file.endswith('.xlsx'):
                    excel_path = os.path.join(root, file)
                    df = pd.read_excel(excel_path)
                    for _, row in df.iterrows():
                        darkweb_entry = Darkweb.query.filter_by(domain=row['Domain']).first()
                        if not darkweb_entry:
                            conductor = dir_name  # 여기서 dir_name은 'function' 바로 아래 폴더의 이름
                            darkweb_entry = Darkweb(
                                conductor=role[conductor],
                                domain=row['Domain']
                            )
                            db.session.add(darkweb_entry)
                            db.session.commit()

                        url = str(row['URL']) if not isinstance(row['URL'], str) else row['URL']
                        html_content = url.replace('http://', '').replace('/', '_')
                        urlweb_entry = DomainToURL(
                            darkweb_id=darkweb_entry.id,
                            url=url,
                            depth=row['Depth'],
                            parameter=row.get('Parameter'),
                            title=row['Title'],
                            keyword=row['Keyword'],
                            html_content=html_content
                        )
                        db.session.add(urlweb_entry)
                    db.session.commit()




