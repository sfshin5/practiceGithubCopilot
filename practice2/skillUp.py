import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import japanize_matplotlib

# 1. 指定したURLのHTMLを取得
url = 'https://www.skillupai.com/skillupai-camp/'
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

# 2. 取得したページから日程（回数）、テーマ、講師およびゲストを抽出
soup = BeautifulSoup(html, 'html.parser')
sessions = soup.find_all('div', class_='session')

dates = []
themes = []
lecturers = []
guests = []

for session in sessions:
    date = session.find('div', class_='date').text.strip()
    theme = session.find('div', class_='theme').text.strip()
    lecturer = session.find('div', class_='lecturer').text.strip()
    guest = session.find('div', class_='guest').text.strip()

    dates.append(date)
    themes.append(theme)
    lecturers.append(lecturer)
    guests.append(guest)

# デバッグ用の出力
print("Dates:", dates)
print("Themes:", themes)
print("Lecturers:", lecturers)
print("Guests:", guests)

# 3. 取得したテーマから、頻出単語を分析して棒グラフで可視化
if themes:
    all_themes = ' '.join(themes)
    print("All Themes:", all_themes)  # デバッグ用の出力

    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='C:/Windows/Fonts/meiryo.ttc').generate(all_themes)

    # 単語の頻度をカウント
    words = all_themes.split()
    word_counts = Counter(words)

    # 上位10単語を取得
    common_words = word_counts.most_common(10)
    words, counts = zip(*common_words)

    # 棒グラフを作成
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts)
    plt.title('テーマの頻出単語')
    plt.xlabel('単語')
    plt.ylabel('頻度')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("テーマが取得できませんでした。")