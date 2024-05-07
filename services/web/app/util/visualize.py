import matplotlib
# GUI 백엔드를 사용하지 않도록 설정
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
from io import BytesIO
import base64

def plot_combined_charts(words):
    # 단어 빈도 계산
    word_list = words.split()
    word_counts = Counter(word_list)
    most_common_words = word_counts.most_common(10)  # 가장 많이 등장하는 10개 단어

    # 막대 그래프와 파이 차트를 동시에 표시하기 위해 서브플롯 사용
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # 막대 그래프 플로팅
    words, frequencies = zip(*most_common_words)
    ax1.bar(words, frequencies, color='green')
    ax1.set_xlabel('Words')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Top Words in Entry')
    ax1.tick_params(axis='x', rotation=45)  # x축 라벨 회전

    # 파이 차트 플로팅
    ax2.pie(frequencies, labels=words, autopct='%1.1f%%', startangle=140)
    ax2.set_title('PieGraph')
    ax2.axis('equal')  # 원형을 유지하기 위해 설정

    # 이미지를 Base64 인코딩 문자열로 변환
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  # 메모리 관리를 위해 그래프 닫기

    return plot_url

def word_cloud(keywords):
    # 워드클라우드 객체 생성
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis')
    
    # 워드클라우드 생성
    cloud = wc.generate(keywords)

    # 이미지 생성
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.imshow(cloud, interpolation='bilinear')
    ax.axis('off')  # 축 제거

    # 이미지를 Base64 인코딩 문자열로 변환
    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  # 메모리 관리를 위해 그래프 닫기

    return plot_url