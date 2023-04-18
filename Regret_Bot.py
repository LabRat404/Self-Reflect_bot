import os
import telebot
import requests
import re
import certifi
import openai
from pymongo import MongoClient
from apiclient.discovery import build
from concurrent.futures import ThreadPoolExecutor

BOT_TOKEN = os.environ.get('bot_token')
CHATID = os.environ.get('chatid')
UAPI = os.environ.get('youtubeAPI')
OpenAPI = os.environ.get('openAI')
bot = telebot.TeleBot(BOT_TOKEN)

def take_record(message):
    print(message)
    #connect to db
    client = MongoClient(uri, tlsCAFile=certifi.where())
    # Access a database and collection
    db = client['test2']
    collection = db.messages
    data = {'name': message.from_user.username, 'text': message.text}
    result = collection.insert_one(data).inserted_id
    print(result)

def send_message(chat_id, text):
    bot_record = bot.send_message(chat_id, text)
    return bot_record

@bot.message_handler(commands=['regret'])
def send_regret(message):
    bot_record = send_message(message.chat.id, "miss her but shes not coming back ㅠ︵ㅠ QAQ")
    take_record(message)
    print(bot_record)
    take_record(bot_record)

@bot.message_handler(commands=['help'])
def send_help(message):
    with ThreadPoolExecutor(max_workers=2) as executor:
        bot_record = executor.submit(send_message, message.chat.id, "Calling 999!, help is coming!")
        take_record(message)
        print(bot_record)
        executor.submit(take_record, bot_record.result())

@bot.message_handler(commands=['visit'])
def send_visit(message):
    url = message.text
    match = re.search(r"/visit\s(https?://\S+)", url)
    response = requests.get(match.group(1))
    with ThreadPoolExecutor(max_workers=2) as executor:
        bot_record = executor.submit(send_message, message.chat.id, response.text)
        take_record(message)
        message = bot_record.result()
        executor.submit(take_record, message)

@bot.message_handler(commands=['GPT'])
def send_GPT(message):
    search_pattern = r'/GPT\s+(.*)'
    match = re.match(search_pattern, message.text).group(1)
    prompt = f"{match}. Reply 'x' if none found and with least token use"
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=120, temperature=0)
    with ThreadPoolExecutor(max_workers=2) as executor:
        bot_record = executor.submit(send_message, message.chat.id, response['choice'][0]['text'])
        take_record(message)
        message = bot_record.result()
        executor.submit(take_record, message)


@bot.message_handler(commands=['youtube'])
def send_youtube(message):
    take_record(message)
    search_pattern = r'/youtube\s+(.*)'
    match = re.match(search_pattern, message.text).group(1)
    youtube = build('youtube', 'v3', developerKey=UAPI)
    requestQ = youtube.search().list(q=match,part='snippet',type='video')
    res = requestQ.execute()
    message_youtube = f"*Top 5 videos related to {match}* \n\n"
    print(res)
    for item in res['items']:
        message_youtube += f"{item['snippet']['title']}\nLink: youtube.com/watch?v={item['id']['videoId']}\n\n"
    with ThreadPoolExecutor(max_workers=2) as executor:
        bot_record = executor.submit(send_message, message.chat.id, message_youtube)
        message = bot_record.result()
        executor.submit(take_record, message)

@bot.message_handler(commands=['book'])
def send_books(message):
    take_record(message)
    url = "https://api.nytimes.com/svc/books/v3/lists/current/hardcover-fiction.json?api-key=DO5UsXoGGEvqm3ZkMC1pFSnRYPq6mGdX"
    response = requests.get(url)
    books = response.json()
    message_book = "*Top 5 books ranked this week on New York Times* \n\n"
    for book in books['results']['books'][:5]:
        message_book += f"*{book['title']}* \nBy author: {book['author']} \nDescription: {book['description']} \n\n\n"
    with ThreadPoolExecutor(max_workers=2) as executor:
        bot_record = executor.submit(send_message, message.chat.id, message_book, parse_mode='Markdown')
        message = bot_record.result()
        executor.submit(take_record, message)

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    if message.text.startswith('/'):
        with ThreadPoolExecutor(max_workers=2) as executor:
            bot_record = executor.submit(send_message, message.chat.id, message.text + "\nCommand not found!!")
            message = bot_record.result()
            executor.submit(take_record, message)
    else:
        with ThreadPoolExecutor(max_workers=2) as executor:
            bot_record = executor.submit(send_message, message.chat.id, message.text)
            take_record(message)
            message = bot_record.result()
            executor.submit(take_record, message)

bot.infinity_polling()