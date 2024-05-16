# S-개발자 2기 1차 교육 프로젝트: 다크웹 크롤러


## 프로젝트 개요:


&nbsp;&nbsp;본 프로젝트는 S-개발자 2기 1차 교육 프로그램의 일환으로 진행된 다크웹 크롤러에 대한 팀 프로젝트입니다. 

&nbsp;&nbsp;본 프로젝트는 학습 목적을 위해 수행되었으며, 어떠한 법적인 위반 행위나 불법적인 목적을 가지고 있지 않음을 명시합니다.



## 프로젝트 설명:


&nbsp;&nbsp;다크웹 크롤러는 다크웹의 다양한 사이트에서 정보를 수집하고 데이터를 정리하여 보관하는 웹 어플리케이션입니다. 

&nbsp;&nbsp;본 프로젝트에서는 팀원들이 협력하여 백엔드, 프론트엔드, 그리고 크롤링 기능을 구현하였습니다. 

| 수집한 전체 도메인 정리 | 각 도메인별 정리 |
|-----------------------|-----------------|
| ![dashboard_1](/assets/img/dashboard_1.png) | ![dashboard_2](/assets/img/dashboard_2.png) |


## 사이트 구조

&nbsp;&nbsp;- **DASHBOARD**: 수집한 다크웹 크롤링 데이터 정리한 것을 도식화하여 대시보드로 제공합니다.

&nbsp;&nbsp;- **TODO**: 분석해야할 총 도메인과 분석한 도메인의 정보를 제공합니다.

&nbsp;&nbsp;- **DEMO**: 초기 버전의 다크웹 크롤러 정적 웹페이지입니다.


## R&R (Roles & Responsibilities)

&nbsp;&nbsp;- **신호 (백엔드, 프론트엔드)**

&nbsp;&nbsp;- **서현 (크롤링 기능 구현, 파일 생성: 43)**

&nbsp;&nbsp;- **민수 (크롤링 기능 구현, 파일 생성, 프론드엔드: 84)**

&nbsp;&nbsp;- **인석 (크롤링 기능 구현, 파일 생성: -)**

&nbsp;&nbsp;- **유빈 (크롤링 기능 구현, 파일 생성: 51)**


## Infrastructure

&nbsp;&nbsp;- **Backend**: Flask

&nbsp;&nbsp;- **Frontend**: HTML, CSS, JS (Apexcharts)

&nbsp;&nbsp;- **Crawling Functionality**: Python (Requests, Beautifulsoap)

&nbsp;&nbsp;- **Database**: FlaskSQLAlchemy (SQLite)

&nbsp;&nbsp;- **Etc**: Python (Pandas, Keybert, Matplotlib) 


## Architecture 구조

![darkwebgo_architecture](/assets/img/darkwebgo_architecture.png)

프로젝트는 다음과 같은 구조로 이루어져 있습니다:

&nbsp;&nbsp;- **Backend**: 

&nbsp;&nbsp;&ensp;- Flask 웹 프레임워크를 사용하여 서버를 구축하고 Domain API를 제공합니다.

&nbsp;&nbsp;- **Frontend**: 

&nbsp;&nbsp;&ensp;- Wordclude, Apexcharts CDN을 활용하여 정리한 크롤링 데이터를 대시보드로 제공합니다.

&nbsp;&nbsp;- **Crawling Functionality**: 

&nbsp;&nbsp;&ensp;- Domain API에 요청하여 onion url를 제공 받습니다. 

&nbsp;&nbsp;&ensp;- Requests, Beatifulsoap를 기반으로 한 Python 스크립트를 사용하여 해당 onion url에 크롤링을 수행합니다. 

&nbsp;&nbsp;&ensp;- Keybert 라이브러리를 활용하여 해당 도메인의 메인 키워드를 추출합니다. 

&nbsp;&nbsp;&ensp;- 각 팀원이 책임을 지고 각 도메인의 사이트 및 하위 Depth 2까지의 사이트를 크롤링합니다.

&nbsp;&nbsp;- **Database**: 

&nbsp;&nbsp;&ensp;- FlaskSQLAlchemy를 사용하여 SQLite 데이터베이스에 수집된 정보를 저장합니다.


## 프로젝트 실행 방법

&nbsp;&nbsp;1. 프로젝트를 클론합니다.
```
git clone https://github.com/DarkwebGO/domain_server.git
cd domain_server
```

&nbsp;&nbsp;2. 백엔드를 실행하기 위해 DB를 생성합니다.
```
cd services/web
flask init-db
flask import-data
```

&nbsp;&nbsp;3. Flask 애플리케이션을 실행해 서버를 호스팅하여 사이트에 접속합니다.
```
python run.py
```

&nbsp;&nbsp;4. (선택) 크롤링 기능을 실행하여 원하는 사이트에서 데이터를 수집합니다. _(크롤링 Python 스크립트 미제공)_


## 기여하기

프로젝트에 기여하고 싶으신 분들은 다음과 같은 방법으로 기여할 수 있습니다:

&nbsp;&nbsp;- 코드 수정 및 개선 제안: GitHub에서 이슈를 제기하고 Pull Request를 보내주세요.

&nbsp;&nbsp;- 문서 작성: 프로젝트의 README 파일이나 문서를 보완하여 프로젝트를 더욱 사용하기 쉽게 만들어주세요.

&nbsp;&nbsp;- 버그 신고: 프로젝트를 사용하면서 발생하는 버그를 GitHub 이슈로 보고해주세요.


## 저작권 (사실 없음)

© 2024 S-개발자 팀 구름망
