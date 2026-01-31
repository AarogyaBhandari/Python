import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

url = 'https://thehimalayantimes.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

trending_topics = soup.find_all('div', class_='latest_style_2_item')

trending_article = []

for each_topic in trending_topics:
    a_tag = each_topic.find('a')
    tag_mark = each_topic.find('span', class_='tag-topic simple')
    if a_tag:
       url = a_tag['href']
       if tag_mark:
          tag = tag_mark.get_text(strip=True)
       else:
          tag = None
      
       trending_article.append(
          {
             'url': url,
              'tag': tag
          })
    

articles_data = []
for article_url in trending_article:
    article_response = requests.get(article_url['url'])
    article_soup = BeautifulSoup(article_response.text, features='html.parser')

    title_tag = article_soup.find('h1', class_='alith_post_title')
    if title_tag:
        title = title_tag.get_text(strip=True)
    else:
        title = None

    content_paragraphs = article_soup.find('div', class_='dropcap column-1 animate-box').find_all('p')
    content = '\n'.join(
        p.get_text(strip=True) 
        for p in content_paragraphs
        )

    articles_data.append({
    'title': title,
    'tag': article_url['tag'],
    'content': content,
    'url': article_url['url'],
    'scraped_at': datetime.now().isoformat()
})

# print(articles_data)

with open('TheHimalayanTimes.json', 'a', encoding='utf-8') as f:
    json.dump(articles_data, f, indent=4)
