from flask import Flask
import threading
import time
from news_scraper import get_news
from telegram_bot import send_message
from config import CHECK_INTERVAL

app = Flask(__name__)
sent_links = set()

def news_loop():
    while True:
        news_list = get_news()
        for n in news_list:
            if n['link'] not in sent_links:
                send_message(n['title'], n['link'], n['summary'])
                sent_links.add(n['link'])
        time.sleep(CHECK_INTERVAL)

# roda loop em thread separada
threading.Thread(target=news_loop, daemon=True).start()

@app.route("/")
def index():
    return "Finance News Bot ativo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
