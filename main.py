import openai
import telebot
import os
from flask import Flask, request

openai.api_key = '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'
TOKEN = '6077876190:AAGTOY8cLkcfIdZqMwCD04B2HtV0h829ucs'
APP_URL = f'https://talkwithgpt.herokuapp.com/{TOKEN}'
bot = telebot.TeleBot("TOKEN")
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
  mess= f'<b>Привет, <u>{message.from_user.first_name} </u>! Я чат-бот. Я могу подсказать тебе возможные ответы на различные вопросы</b>'
  bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(func=lambda _: True)
def handle_message(message):
 response = openai.Completion.create(
 model="text-davinci-003",
  prompt=message.text,
  temperature=0.5,
  max_tokens=1000,
  top_p=1.0,
  frequency_penalty=0.5,
  presence_penalty=0.0,
  )

 bot.send_message(chat_id=message.from_user.id, text=response['choices'][0]['text'])

@server.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return '!', 200

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

