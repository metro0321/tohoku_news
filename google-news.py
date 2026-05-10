import requests
from bs4 import BeautifulSoup
import feedparser

# 東北地方の都道府県リスト
prefectures = ["青森", "岩手", "宮城", "秋田", "山形", "福島"]

# ここに抽出したいキーワードを追加します
target_keywords = ["車中泊", "キャンプ", "アウトドア", "旅行", "観光", "見頃", "道の駅"]  # 例: 車中泊関連のキーワード

news_list = []
seen_urls = set()

def get_og_image(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
    except:
        pass
    return "https://via.placeholder.com/120x80.png?text=News"

for pref in prefectures:
    # GoogleニュースのRSSフィード
    rss_url = f"https://news.google.com/rss/search?q={pref}&ceid=JP:ja&hl=ja"
    
    try:
        feed = feedparser.parse(rss_url)
        print(f"Fetching news for {pref}... Found {len(feed.entries)} results")
        
        for item in feed.entries:
            title = item.get('title', '').strip()
            
            # 実際の記事URLを取得（Googleニュースのリンクから）
            href = None
            for link in item.get('links', []):
                if link.get('rel') == 'alternate':
                    href = link.get('href')
                    break
            if not href:
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

print(f"Total news collected: {len(news_list)}")

# HTML生成
html = "<html><head><meta charset='utf-8'><title>東北地方ニュースまとめ</title><style>body{font-family:\"Segoe UI\",\"Hiragino Sans\",sans-serif;background-color:#f9f9f9;margin:0;padding:20px;}h1{text-align:center;color:#2c3e50;}ul{list-style:none;padding:0;max-width:800px;margin:20px auto;}li{background:#fff;margin:10px 0;padding:15px;border-radius:8px;box-shadow:0 2px 5px rgba(0,0,0,0.1);transition:transform 0.2s;}li:hover{transform:translateY(-3px);}a{text-decoration:none;color:#2980b9;font-weight:bold;}a:hover{color:#e74c3c;}</style></head><body>"
html += "<h1>東北地方ご当地ニュース</h1><ul>"
for title, href in news_list:
    html += f"<li><a href='{href}' target='_blank'>{title}</a></li>"
html += "</ul></body></html>"

with open("docs/index.html", "w", encoding="utf-8-sig") as f:
    f.write(html)