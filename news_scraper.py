import requests
from bs4 import BeautifulSoup
from config import NEWS_SOURCES

def get_news():
    news_list = []
    for url in NEWS_SOURCES:
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(r.text, 'html.parser')
            for item in soup.select("a.title"):
                title = item.get_text()
                link = item.get('href')
                news_list.append(f"{title}\n{link}")
        except Exception as e:
            print(f"Erro ao buscar notícias: {e}")
    return news_list
