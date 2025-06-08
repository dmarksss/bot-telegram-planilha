import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from telegram.ext import Application, CommandHandler

print("Iniciando o bot...")

try:
    # 🔐 Escopos de autenticação (Planilhas + Drive)
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # 🔐 Carrega credenciais e conecta com Google Sheets
    credenciais = Credentials.from_service_account_file("credenciais.json", scopes=scopes)
    cliente = gspread.authorize(credenciais)

    # 📄 Abre a planilha e aba
    planilha = cliente.open("bot_teste")
    aba = planilha.worksheet("Entradas")

    # 🔸 Comando /start
    async def start(update, context):
        await update.message.reply_text("✅ Bot conectado com sucesso!")

    # 🔸 Comando /dados
    async def dados(update, context):
        registros = aba.get_all_records()
        df = pd.DataFrame(registros)
        if df.empty:
            await update.message.reply_text("⚠️ Nenhum dado encontrado.")
        else:
            primeira_linha = df.head(1).to_string(index=False)
            await update.message.reply_text(f"Dado da planilha:\n{primeira_linha}")

    # 🤖 Token do Bot do Telegram
    TOKEN = "7729065625:AAFQoUER5wO6Us5sC5_PzgUzFFaK7o9dodM"

    # 🚀 Inicializa o bot
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dados", dados))
    app.run_polling()

except Exception as e:
    print("Erro encontrado:")
    print(e)
