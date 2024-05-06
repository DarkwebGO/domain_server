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
    @app.cli.command("init-db")
    def init_db():
        db.drop_all()
        db.create_all()
        print('Initialized the database.')

    @app.cli.command("import-data")
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
    dir_names = []
    for root, dirs, files in os.walk(base_directory):
        # function의 바로 아래 하위 폴더인 경우 변수 direct_function_dir_name에 저장. 
        for directory in dirs:
            directory_path = os.path.join(root, directory)
            dir_name = os.path.basename(root)  # 상위 폴더의 이름 추출
            if dir_name not in dir_names and dir_name != "function":  # 중복 방지를 위해 확인
                dir_names.append(dir_name)  # 새로운 상위 폴더 이름 추가
                print(dir_name)
            for file in os.listdir(directory_path):
                if file.endswith('.xlsx'):
                    excel_path = os.path.join(directory_path, file)
                    df = pd.read_excel(excel_path)
                    for _, row in df.iterrows():
                        darkweb_entry = Darkweb.query.filter_by(domain=row['Domain']).first()
                        if not darkweb_entry:
                            conductor = dir_name
                            darkweb_entry = Darkweb(
                                conductor= conductor,
                                domain=row['Domain']
                            )
                            db.session.add(darkweb_entry)
                            db.session.commit()
                        # URL이 문자열이 아닌 경우 처리
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


