import requests
from bs4 import BeautifulSoup
import feedparser

# 東北地方の都道府県リスト
prefectures = ["青森", "岩手", "宮城", "秋田", "山形", "福島"]

# ここに抽出したいキーワードを追加します
target_keywords = ["車中泊", "キャンプ", "アウトドア", "旅行", "観光", "見頃", "道の駅"]  # 例: 車中泊関連のキーワード

news_list = []
seen_urls = set()

for pref in prefectures:
    # GoogleニュースのRSSフィード
    rss_url = f"https://news.google.com/rss/search?q={pref}&ceid=JP:ja&hl=ja"
    
    try:
        feed = feedparser.parse(rss_url)
        print(f"Fetching news for {pref}... Found {len(feed.entries)} results")
        
        for item in feed.entries:
            title = item.get('title', '').strip()
            href = item.get('link', '')
            
            if not title or not href:
                continue
            if href in seen_urls:
                continue

            lower_title = title.lower()
            if target_keywords:
                if not any(keyword.lower() in lower_title for keyword in target_keywords):
                    continue

            seen_urls.add(href)
            news_list.append((title, href))
    except Exception as e:
        print(f"Error fetching news for {pref}: {e}")

# HTML生成
html = "<html><head><meta charset='utf-8'><title>東北地方ニュースまとめ</title></head><body>"
html += "<h1>東北地方ご当地ニュース</h1><ul>"
for title, href in news_list:
    html += f"<li><a href='{href}' target='_blank'>{title}</a></li>"
html += "</ul></body></html>"

print(f"Total news collected: {len(news_list)}")

with open("docs/index.html", "w", encoding="utf-8-sig") as f:
    f.write(html)