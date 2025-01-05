# Web スクレイピングを行うプログラム
# 対象ページ：https://www.skillupai.com/skillupai-camp/
# 手順
# 1. 指定したURLのHTMLを取得
# 2. 取得したページから日程（回数）、テーマ、講師およびゲストを抽出
# 3. 取得したテーマから、頻出単語を分析して棒グラフで可視化
# ライブラリのインポート
import requests
from bs4 import BeautifulSoup
import MeCab
import collections
import matplotlib.pyplot as plt
import japanize_matplotlib
# スクレイピング対象のURL
url = 'https://www.skillupai.com/skillupai-camp/'
# ページの取得
response = requests.get(url)
response.encoding = response.apparent_encoding
# ページの解析
soup = BeautifulSoup(response.text, 'html.parser')
# tr内のテキストを全て取得
trs = soup.find_all('tr')
### 回数及び日付の取得
# trsから<th>タグ内のテキストを取得
th_list = [tr.find('th').text for tr in trs]
# th_listからテキストが"日程"となっている要素を削除
th_list = [th for th in th_list if th != '日程']
# th_listから¥nを削除
th_list = [th.replace('¥n', '') for th in th_list]
# th_listから”※受付終了”の文字列を削除
th_list = [th.replace('※受付終了', '') for th in th_list]
# ”回”の後ろに空白を挿入
th_list = [th.replace('回', '回') for th in th_list]
### テーマ、講師、ゲストを取得
# trs内のthemeタグ, teacherタグ, guestタグのテキストを取得
# trs内に該当タグが見つからない場合はスキップ
theme_list = []
teacher_list = []
guest_list = []

for tr in trs:
    try:
        theme_list.append(tr.find('td', class_='theme').text)
        teacher_list.append(tr.find('td', class_='teacher').text)
        guest_list.append(tr.find('td', class_='guest').text)
    except:
        pass
# theme_listから¥nを削除
theme_list = [theme.replace('¥n', '') for theme in theme_list]
# theme_listから”詳細はこちら”の文字列を削除
theme_list = [theme.replace('詳細はこちら', '') for theme in theme_list]
# theme_listから”再配信”の文字列を削除
theme_list = [theme.replace('再配信', '') for theme in theme_list]
# theme_listから”ライブ配信”の文字列を削除
theme_list = [theme.replace('ライブ配信', '') for theme in theme_list]
# guest_listの¥u3000を空白に置換
guest_list = [guest.replace('¥u3000', ' ') for guest in guest_list]

### theme_list内に含まれる単語の頻度を解析
# Mecabをインスタンス化
mecab = MeCab.Tagger()
# theme_list内の名詞の単語を抽出
words = []
for theme in theme_list:
    node = mecab.parseToNode(theme)
    while node:
        if node.feature.split(',')[0] == '名詞':
            words.append(node.surface)
            node = node.next

# 単語の出現頻度を解析
counter = collections.Counter(words)

### 出現頻度が3以上の単語で棒グラフを作成
# 出現頻度が3以上の単語を抽出
over_three_words = []
for word, cnt in counter.items():
    if cnt >= 3:
        over_three_words.append(word)
# 出現頻度が高い順にソート
over_three_words.sort(key=lambda x: counter[x], reverse=True)
# 棒グラフの作成
plt.figure(figsize=(12, 6))
plt.bar(over_three_words, [counter[word] for word in over_three_words])
plt.xticks(rotation=90)
# グラフの下の余白を広くする
plt.subplots_adjust(bottom=0.22)
plt.show()