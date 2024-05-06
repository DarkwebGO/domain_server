import matplotlib
# GUI 백엔드를 사용하지 않도록 설정
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from collections import Counter
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