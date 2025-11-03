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
        try:
            print("[INFO] Buscando notícias...")
            news_list = get_news()
            print(f"[INFO] Notícias encontradas: {len(news_list)}")
            
            if not news_list:
                print("[INFO] Nenhuma notícia nova encontrada.")
            
            for n in news_list:
                if n['link'] not in sent_links:
                    print(f"[INFO] Enviando notícia: {n['title']}")
                    try:
                        send_message(n['title'], n['link'], n['summary'])
                    except Exception as e:
                        print(f"[ERRO] Falha ao enviar notícia: {e}")
                    sent_links.add(n['link'])
                else:
                    print(f"[INFO] Notícia já enviada: {n['title']}")
            
            # Reset diário dos links enviados
            current_hour = time.localtime().tm_hour
            if current_hour == 0:
                sent_links.clear()
                print("[INFO] Reset diário de notícias enviadas.")

        except Exception as e:
            print(f"[ERRO] Ocorreu um erro no loop de notícias: {e}")

        time.sleep(CHECK_INTERVAL)

# roda loop em thread separada
threading.Thread(target=news_loop, daemon=True).start()

@app.route("/")
def index():
    return "Finance News Bot ativo!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
