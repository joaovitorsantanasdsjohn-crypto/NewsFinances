import feedparser
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from config import NEWS_FEEDS, KEYWORDS, TRUSTED_SOURCES

def fetch_rss_news():
    news_list = []
    for feed_url in NEWS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            link = entry.link
            # filtragem por palavras-chave
            if any(k.lower() in title.lower() for k in KEYWORDS):
                news_list.append({"title": title, "link": link, "source": urlparse(link).netloc})
    return news_list

def fetch_url_summary(url):
    """Extrai resumo da página, se possível"""
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        # tenta pegar o parágrafo principal
        p = soup.find("p")
        return p.get_text() if p else ""
    except:
        return ""

def get_news():
    news = fetch_rss_news()
    # remove duplicadas e prioriza fontes confiáveis
    seen_titles = set()
    filtered_news = []
    for n in sorted(news, key=lambda x: x['source'] in TRUSTED_SOURCES, reverse=True):
        if n['title'] not in seen_titles:
            n['summary'] = fetch_url_summary(n['link'])
            filtered_news.append(n)
            seen_titles.add(n['title'])
    return filtered_news
