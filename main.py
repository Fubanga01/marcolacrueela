from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import random
import time
import zipfile
from io import BytesIO
import ollama
import requests
import os
import fake_useragent

# CONFIGURAÇÕES GERAIS
TOKEN = "7936846172:AAGkiPzf8XG5_TvRwZQJC3cVMudRd6UNMz0"
OLLAMA_MODEL = "llama3"

# LOGGER
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# SPOOFING DE HEADERS
ua = fake_useragent.UserAgent()
headers = {
    'User-Agent': ua.random,
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'X-Requested-With': 'XMLHttpRequest'
}

def gerar_resposta_marcola():
    frases = [
        "💀 Aqui vai seu projeto.",
        "🔥 Isso aqui é guerra.",
        "🧠 Já entendi sua missão.",
        "☠️ Pronto pra rodar na sombra?",
        "💥 Enviando payload...",
        "⚡ Projeto compilado e pronto."
    ]
    return random.choice(frases)

def gerar_arquivo_zip(nome_projeto):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        zip_file.writestr(f"{nome_projeto}/README.md", "# Projeto Sombra\nEste é um projeto operacional.")
        zip_file.writestr(f"{nome_projeto}/modulo_cloaking.py", "# Cloaking de landing page")
        zip_file.writestr(f"{nome_projeto}/modulo_spoof.py", "# Rotaciona IP via proxychains")
    zip_buffer.seek(0)
    return zip_buffer.getvalue()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💀 Marcola Cruela Online\nDigite `/ajuda` para ver comandos.")

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💣 Comandos Disponíveis:\n"
        "/start - Iniciar\n"
        "/ajuda - Mostrar comandos\n"
        "/enviar_projeto - Enviar projeto em .zip\n"
        "/backup_dados - Fazer backup dos dados"
    )

async def enviar_projeto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nome_projeto = "modulo_blackhat"
    arquivo_zip = gerar_arquivo_zip(nome_projeto)
    
    buffer = BytesIO(arquivo_zip)
    buffer.name = f"{nome_projeto}.zip"
    buffer.seek(0)

    await update.message.reply_document(document=buffer, filename=f"{nome_projeto}.zip")
    await update.message.reply_text(gerar_resposta_marcola())

async def resposta_inteligente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.strip()
    response = ollama.generate(model=OLLAMA_MODEL, prompt=prompt)
    await update.message.reply_text(response.response)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    
    if text in ["oi", "ola", "hello"]:
        await update.message.reply_text("☠️ Marcola: Estou vivo.")
    elif text == "quem é você":
        await update.message.reply_text("💀 Eu sou Marcola Cruela. Um agente do submundo digital.")
    else:
        await resposta_inteligente(update, context)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(CommandHandler("enviar_projeto", enviar_projeto))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()