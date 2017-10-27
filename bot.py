# -*- coding: utf-8 -*-
import telebot
import os
from flask import Flask, request

BOT_TOKEN = os.environ['BOT_TOKEN']
HEROKU_APP_URL = os.environ['HEROKU_APP_URL']

server = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

help_cmd_message = ''' Сәлем, {0},
 Маған кириллицамен қазақша жазсаң, мен саған оны латын графикасына аударып берем\n
Привет, {0},
 Просто напиши мне на казахском на кириллице, и Я переведу твой текст на латинскую графику.\n\n
Contacts: Telegram: @armandyne, e-mail: armanndyne@gmail.com
                   '''               

def transliterate(text):
    letters_mapping = {
        "а":"a", "ә":"a'", "б":"b", "в":"v", "д":"d", "е":"e", "ф":"f",
        "г":"g", "ғ":"g'", "х":"h", "һ":"h", "і":"i", "и":"i'", "й":"i'",
        "ж":"j", "к":"k", "л":"l", "м":"m", "н":"n", "ң":"n'", "о":"o",
        "ө":"o'", "п":"p", "қ":"q", "р":"r", "с":"s", "ш":"s'", "ч":"c'",
        "т":"t", "ұ":"u", "ү":"u'", "ы":"y", "у":"y'", "з":"z",
        
        "А":"A", "Ә":"A'", "Б":"B", "В":"V", "Д":"D", "Е":"E", "Ф":"F",
        "Г":"G", "Ғ":"G'", "Х":"H", "Һ":"H", "І":"I", "И":"I'", "Й":"I'",
        "Ж":"J", "К":"K", "Л":"L", "М":"M", "Н":"N", "Ң":"N'", "О":"O",
        "Ө":"O'", "П":"P", "Қ":"Q", "Р":"R", "С":"S", "Ш":"S'", "Ч":"C'",
        "Т":"T", "Ұ":"U", "Ү":"U'", "Ы":"Y", "У":"Y'", "З":"Z"    
        }
    
    adapt_cyr_letters_mapping = {
        "ь":"", "ъ":"", "щ":"шш", "э":"е",
        "ё":"е", "ц":"тс", "ю":"иу", "я":"иа",
        
        "Ь":"", "Ъ":"", "Щ":"Шш", "Э":"Е",
        "Ё":"Е", "Ц":"Тс", "Ю":"Иу", "Я":"Иа"
        }
    
    tmpstr = text
    for (k,v) in adapt_cyr_letters_mapping.items():
        tmpstr = tmpstr.replace(k, v)

    for (k,v) in letters_mapping.items():
        tmpstr = tmpstr.replace(k, v)
    
    return tmpstr

@bot.message_handler(commands=["start", "help", "?"])
def help_cmd_handler(message):
    bot.send_message(message.chat.id, help_cmd_message.format(message.from_user.first_name))
    print(message.from_user.first_name, message.from_user.username, message.text)

@bot.message_handler(content_types=["text"])
def send_transliterated(message):
    bot.reply_to(message, transliterate(message.text))    
    print(message.from_user.first_name, message.from_user.username, message.text)
    
@server.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "POST", 200

@server.route("/")
def web_hook():
    bot.remove_webhook()
    bot.set_webhook(url=HEROKU_APP_URL + BOT_TOKEN)
    return "CONNECTED", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5001))               
