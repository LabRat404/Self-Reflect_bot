from telegram import Update, request
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
import os
import telebot
import requests
import re
BOT_TOKEN = os.environ.get('bot_token')
CHATID = os.environ.get('chatid')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['regret'])
def send_regret(message):
    bot.send_message(message.chat.id, "miss her but shes not coming back ( ･᷄ ︵･᷅ )")


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Calling 999!, help is coming!")


@bot.message_handler(commands=['visit'])
def send_visit(message):
    url = message.text
    match = re.search(r"/visit\s(https?://\S+)", url)
    response = requests.get(match.group(1))
    bot.send_message(message.chat.id, response.text)


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.send_message(message.chat.id, message.text)

bot.infinity_polling()



