import requests
import time
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, MAX_MESSAGES_PER_HOUR
from deep_translator import GoogleTranslator

sent_messages = []

def translate_text(text, target_lang="pt"):
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print("Erro na tradução:", e)
        return text  # retorna original se houver erro

def send_message(title, link, summary=""):
    global sent_messages
    # limpa mensagens antigas (>1h)
    sent_messages = [t for t in sent_messages if time.time() - t < 3600]

    if len(sent_messages) >= MAX_MESSAGES_PER_HOUR:
        print("Limite de mensagens por hora atingido.")
        return

    # traduz título e resumo
    title_pt = translate_text(title)
    summary_pt = translate_text(summary) if summary else ""

    text = f"{title_pt}\n{link}\n{summary_pt}"
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text}

    try:
        r = requests.post(url, data=data)
        if r.status_code == 200:
            sent_messages.append(time.time())
            print(f"Mensagem enviada: {title_pt[:50]}...")
        else:
            print("Erro ao enviar mensagem:", r.text)
    except Exception as e:
        print("Erro no envio Telegram:", e)
