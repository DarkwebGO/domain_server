import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os, json
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

        # url이 depth가 기준보다 높거나, 해당 url이 이미 방문했을 때 제외
        if current_depth > max_depth or current_url in visited:
            continue
        visited.add(current_url)
        print(f"Visiting {current_url} at depth {current_depth}")
        try:
            response = requests.get(current_url, proxies=proxies, allow_redirects=True)
            if response.status_code == 200:
                filename = sanitize_filename(current_url)
                file_path = os.path.join(save_path, filename)

                # html 파일 저장하기
                # with open(file_path, 'wb') as fd:
                    # fd.write(response.content)
                
                soup = BeautifulSoup(response.content, 'html.parser')
                title = str(soup.title).replace("<title>","").replace("</title>", "")
                print(f"url : {current_url} , Title: {title}")

                # URL 구성요소 파싱
                parsed_url = urlparse(current_url)
                domain = parsed_url.netloc
                parameters = parse_qs(parsed_url.query)
                words = ' '.join(soup.get_text().split())

                # 데이터 저장
                # domain, url, depth, parameter, title, words, html-contents
                data_dict = {'domain':domain, 'url':current_url, 'depth':current_depth, 'parameter':parameters, 'title':title, 'words':words, 'html-contents':str(response.content)}
                print(json.dumps(data_dict, indent=4, sort_keys=True))

                # json 파일 저장
                path = save_path + "/" + str(filename).replace('.html', '') + ".json"
                with open(path, 'w') as fd:
                    json.dump(data_dict, fd, indent=4)

                # depth가 가능하다면 url을 queue에 넣기
                if current_depth < max_depth:
                    links = [urljoin(current_url, link.get('href')) for link in soup.find_all('a') if link.get('href')]
                    for link in links:
                        if link not in visited and link != current_url:
                            queue.append((link, current_depth + 1))
            response.close()
        except Exception as e:
            print(f"Error accessing {current_url}: {str(e)}")

save_path = ".//dark-web-database"
onions_list = []

if __name__ == "__main__":
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open("onions.txt", "rb") as file:
        onions = file.read()
        for onion_link in onions.decode("utf-8").split('\n'):
            onion_url = "http://" + onion_link[:-1]
            onions_list.append(onion_url)

    # txt 파일에 있는 url들 중 일부 크롤링(각각 depth 2까지)
    for link in onions_list[10000:10002]:
        crawl_onion_bfs(link, 2, proxies, save_path)