import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os
from collections import deque
import pandas as pd

# 프록시 설정, 저장 경로, 디렉터리 확인 및 파일에서 URL 읽기와 동일
proxies = {
    "http" : "socks5h://127.0.0.1:9150",
    "https" : "socks5h://127.0.0.1:9150"
}

def sanitize_filename(url):
    return url.replace("http://", "").replace("/", "_") + ".html"

def crawl_onion_bfs(start_url, max_depth, proxies, save_path):
    queue = deque([(start_url, 0)])  # (URL, depth)
    visited = set()
    data = []  # 데이터를 저장할 리스트

    while queue:
        current_url, current_depth = queue.popleft()
        if current_depth > max_depth or current_url in visited:
            continue
        visited.add(current_url)

        print(f"Visiting {current_url} at depth {current_depth}")
        
        try:
            response = requests.get(current_url, proxies=proxies, allow_redirects=True)
            if response.status_code == 200:
                filename = sanitize_filename(current_url)
                file_path = os.path.join(save_path, filename)
                with open(file_path, 'wb') as fd:
                    fd.write(response.content)

                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else 'No title'
                print(f"Visited {current_url} - Title: {title}")

                # URL 구성요소 파싱
                parsed_url = urlparse(current_url)
                domain = parsed_url.netloc
                parameters = parse_qs(parsed_url.query)
                words = ' '.join(soup.get_text().split())

                # 데이터 저장
                data.append([domain, current_url, current_depth, parameters, title, words])

                if current_depth < max_depth:
                    links = [urljoin(current_url, link.get('href')) for link in soup.find_all('a') if link.get('href')]
                    for link in links:
                        if link not in visited and link != current_url:
                            queue.append((link, current_depth + 1))
            response.close()
        except Exception as e:
            print(f"Error accessing {current_url}: {str(e)}")

    # 데이터프레임 생성 및 엑셀 파일로 저장
    df = pd.DataFrame(data, columns=['Domain', 'URL', 'Depth', 'Parameters', 'Title', 'Words'])
    df.to_excel(os.path.join(save_path, 'crawl_results.xlsx'), index=False)

save_path = "C:\\Users\\mandeuk\\Desktop\\S-Dev\\Darkweb Crawler\\0425_html_2"
if not os.path.exists(save_path):
    os.makedirs(save_path)

with open("C:\\Users\\mandeuk\\Desktop\\S-Dev\\Darkweb Crawler\\0425\\onions.txt", "r") as file:
    lines = file.readlines()
    onion_url = "http://" + lines[14].strip()

# BFS 크롤링 시작
crawl_onion_bfs(onion_url, 2, proxies, save_path)
