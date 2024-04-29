import csv
import json
import os
import random
from collections import deque
from urllib.parse import parse_qs, urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 프록시 설정, 저장 경로, 디렉터리 확인 및 파일에서 URL 읽기와 동일
proxies = {"http": "socks5h://127.0.0.1:9150", "https": "socks5h://127.0.0.1:9150"}


def sanitize_filename(url):
    return url.replace("http://", "").replace("/", "_") + ".html"


def crawl_onion_bfs(start_url, max_depth, proxies, save_path, csv_path):
    queue = deque([(start_url, 0)])  # (URL, depth)
    visited = set()
    data = []  # 데이터를 저장할 리스트
    excel_file_path = os.path.join(csv_path, "crawl_results.xlsx")

    if os.path.exists(excel_file_path):
        df = pd.read_excel(excel_file_path)
        data = df.values.tolist()  # DataFrame을 리스트의 리스트로 변환
    else:
        data = []

    while queue:
        current_url, current_depth = queue.popleft()
        if current_depth > max_depth or current_url in visited:
            continue
        visited.add(current_url)
        try:
            response = requests.get(current_url, proxies=proxies, allow_redirects=True)
            if response.status_code == 200:
                filename = sanitize_filename(current_url)
                file_path = os.path.join(save_path, filename)
                with open(file_path, "wb") as fd:
                    fd.write(response.content)
                soup = BeautifulSoup(response.content, "html.parser")
                title = soup.title.string if soup.title else "No title"
                parsed_url = urlparse(current_url)
                domain = parsed_url.netloc
                parameters = parse_qs(parsed_url.query)
                words = " ".join(soup.get_text().split())

                data.append(
                    [domain, current_url, current_depth, parameters, title, words]
                )

                df.to_excel(os.path.join(save_path, "crawl_results.xlsx"), index=False)
                if current_depth < max_depth:
                    links = [
                        urljoin(current_url, link.get("href"))
                        for link in soup.find_all("a")
                        if link.get("href")
                    ]
                    for link in links:
                        if link not in visited and link != current_url:
                            queue.append((link, current_depth + 1))
            response.close()

        except Exception as e:
            print(f"Error accessing {current_url}: {str(e)}")
        df = pd.DataFrame(
            data,
            columns=["Domain", "URL", "Depth", "Parameters", "Title", "Words"],
        )
        df.to_excel(excel_file_path, index=False)


save_path_html = "C:\\Users\\psh00\\Desktop\\박서현\\활동\\교육\\S개발자2기\\다크웹 크롤링\\tor\\html"
csv_path = (
    "C:\\Users\\psh00\\Desktop\\박서현\\활동\\교육\\S개발자2기\\다크웹 크롤링\\tor\\csv"
)
if not os.path.exists(save_path_html):
    os.makedirs(save_path_html)
if not os.path.exists(csv_path):
    os.makedirs(csv_path)


link_dict = {}
with open(
    "C:\\Users\\psh00\\Desktop\\박서현\\활동\\교육\\S개발자2기\\다크웹 크롤링\\tor_crawl\\onions.txt",
    "r",
) as file:
    data = file.read()
    lines = data.split("\n")
    for num in range(len(lines)):
        link_dict[num] = "http://" + lines[num]


# BFS 크롤링 시작
# 랜덤 url선택 후 크롤링 시작
for i in random.sample(list(link_dict.keys()), 3):
    print(i, link_dict[i])
    crawl_onion_bfs(link_dict[i], 2, proxies, save_path_html, csv_path)
