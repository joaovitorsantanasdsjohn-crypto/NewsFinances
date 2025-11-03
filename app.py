from flask import Flask
import threading
import time
from news_scraper import get_news
from telegram_bot import send_message

app = Flask(__name__)

CHECK_INTERVAL = 60 * 10  # verifica a cada 10 minutos
sent_links = set()

def news_loop():
    while True:
        news_list = get_news()
        for news in news_list:
            link = news.split("\n")[-1]
            if link not in sent_links:
                send_message(news)
                sent_links.add(link)
        time.sleep(CHECK_INTERVAL)

# Roda o loop de notícias em thread separada
threading.Thread(target=news_loop, daemon=True).start()

@app.route("/")
def index():
    return "Finance News Bot ativo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
