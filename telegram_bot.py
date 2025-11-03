import requests
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MAX_MESSAGES_PER_HOUR

sent_messages = []

def send_message(message):
    global sent_messages

    # Limpa mensagens antigas (mais de 1 hora)
    sent_messages = [t for t in sent_messages if time.time() - t < 3600]

    if len(sent_messages) >= MAX_MESSAGES_PER_HOUR:
        print("Limite de mensagens por hora atingido.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}

    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            sent_messages.append(time.time())
            print(f"Mensagem enviada: {message[:50]}...")
        else:
            print("Erro ao enviar mensagem:", r.text)
    except Exception as e:
        print("Erro no envio Telegram:", e)
