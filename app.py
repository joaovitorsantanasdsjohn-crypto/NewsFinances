from flask import Flask
import threading
import time
from news_scraper import get_news
from telegram_bot import send_message
from config import CHECK_INTERVAL

app = Flask(__name__)
sent_links = set()

# Função principal do loop de notícias
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
                        send_message(n['title'], n['link'], n.get('summary', ''))
                    except Exception as e:
                        print(f"[ERRO] Falha ao enviar notícia: {e}")
                    sent_links.add(n['link'])
                else:
                    print(f"[INFO] Notícia já enviada: {n['title']}")

            # Reset diário dos links enviados (à meia-noite)
            current_hour = time.localtime().tm_hour
            if current_hour == 0:
                sent_links.clear()
                print("[INFO] Reset diário de notícias enviadas.")

        except Exception as e:
            print(f"[ERRO] Ocorreu um erro no loop de notícias: {e}")
            reconnect_loop()  # tenta reconectar automaticamente

        time.sleep(CHECK_INTERVAL)

# Função de reconexão com tentativas automáticas
def reconnect_loop():
    print("[AVISO] Tentando reconectar o loop de notícias...")
    for i in range(1, 6):  # tenta 5 vezes antes de desistir
        try:
            time.sleep(10 * i)  # espera progressiva (10s, 20s, 30s...)
            print(f"[RECONEXÃO] Tentativa {i}/5...")
            news_list = get_news()
            if news_list:
                print("[RECONEXÃO] Conexão restabelecida com sucesso!")
                return  # sai da função se der certo
        except Exception as e:
            print(f"[ERRO] Falha na tentativa de reconexão {i}: {e}")

    print("[FATAL] Não foi possível reconectar após várias tentativas. Reiniciando loop...")
    # Reinicia o loop completamente (sem encerrar o Flask)
    threading.Thread(target=news_loop, daemon=True).start()

# Roda o loop de notícias em thread separada
threading.Thread(target=news_loop, daemon=True).start()

@app.route("/")
def index():
    return "Finance News Bot ativo e com reconexão automática!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
