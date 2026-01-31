
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

# Target URL
url = 'https://english.onlinekhabar.com/'

# Fetch the page
response = requests.get(url)
soup = BeautifulSoup(response.text, features='html.parser')

trending_topics = soup.find_all('div', class_='ok-news-post rtl-post-small')

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

    title = article_soup.find('h1').get_text(strip=True)
    content_paragraphs = article_soup.find('div', class_='post-content-wrap').find_all('p')
    content = '\n\n'.join(
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

with open('Online_Khabar.json', 'a', encoding='utf-8') as f:
    json.dump(articles_data, f, indent=4)
#w for first time, a for append 