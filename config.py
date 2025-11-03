# =============================
# Configuração Finance News Bot
# =============================

# Token do seu bot Telegram
TELEGRAM_TOKEN = "7964245740:AAH7yN95r_NNQaq3OAJU43S4nagIAcgK2w0"

# Chat ID do Telegram
TELEGRAM_CHAT_ID = "6370166264"

# Limite de mensagens por hora para evitar flood
MAX_MESSAGES_PER_HOUR = 5

# Intervalo de verificação de notícias (segundos)
CHECK_INTERVAL = 60 * 10  # 10 minutos

# Palavras-chave de interesse para filtrar notícias
KEYWORDS = [
    "forex", "bitcoin", "ethereum", "ações", "commodities",
    "economia", "banco central", "Fed", "política econômica"
]

# RSS feeds e agregadores iniciais (pode adicionar mais)
NEWS_FEEDS = [
    "https://news.google.com/rss/search?q=forex",
    "https://news.google.com/rss/search?q=cryptocurrency",
    "https://news.google.com/rss/search?q=stocks",
    "https://news.google.com/rss/search?q=commodities",
    "https://news.google.com/rss/search?q=economy"
]

# Fontes confiáveis prioritárias
TRUSTED_SOURCES = [
    "investing.com",
    "bloomberg.com",
    "reuters.com",
    "forexfactory.com",
    "coindesk.com"
    "binance.com"
]
