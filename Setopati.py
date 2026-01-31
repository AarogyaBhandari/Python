
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

BASE_URL = "https://en.setopati.com"
url = BASE_URL + "/"

response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")

bishesh_sections = soup.find_all("div", class_="bishesh")

trending_articles = []
seen_urls = set()

for section in bishesh_sections:
    right_col = section.find("div", class_="bishesh-right")
    if right_col:
        featured = right_col.find("div", class_="featured-item")
        if featured:
            a = featured.find("a", href=True)
            tag = featured.find("span", class_="tags")
            title = featured.find("span", class_="main-title")

            if a:
                link = a["href"]
                if link not in seen_urls:
                    trending_articles.append({
                        "url": link,
                        "tag": tag.get_text(strip=True) if tag else None,
                        "title": title.get_text(strip=True) if title else None
                    })
                    seen_urls.add(link)

        for item in right_col.find_all("div", class_="items media"):
            a = item.find("a", href=True)
            tag = item.find("span", class_="tags")
            title = item.find("span", class_="main-title")

            if a:
                link = a["href"]
                if link not in seen_urls:
                    trending_articles.append({
                        "url": link,
                        "tag": tag.get_text(strip=True) if tag else None,
                        "title": title.get_text(strip=True) if title else None
                    })
                    seen_urls.add(link)

    left_col = section.find("div", class_="bishesh-left")
    if left_col:
        for item in left_col.find_all("div", class_="items media"):
            a = item.find("a", href=True)
            tag = item.find("span", class_="tags")
            title = item.find("span", class_="main-title")

            if a:
                link = a["href"]
                if link not in seen_urls:
                    trending_articles.append({
                        "url": link,
                        "tag": tag.get_text(strip=True) if tag else None,
                        "title": title.get_text(strip=True) if title else None
                    })
                    seen_urls.add(link)


articles_data = []

for article in trending_articles:
    res = requests.get(article["url"], headers={"User-Agent": "Mozilla/5.0"})
    article_soup = BeautifulSoup(res.text, "html.parser")

    content_div = article_soup.find("div", class_="editor-box")
    content = "\n\n".join(
        p.get_text(strip=True)
        for p in content_div.find_all("p")
    ) if content_div else ""

    articles_data.append({
        "title": article["title"],
        "tag": article["tag"],
        "content": content,
        "url": article["url"],
        "scraped_at": datetime.now().isoformat()
    })

with open("Setopati.json", "a", encoding="utf-8") as f:
    json.dump(articles_data, f, indent=4, ensure_ascii=False)


