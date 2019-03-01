# -*- coding: utf-8 -*-
import telebot
import os
from flask import Flask, request

BOT_TOKEN = os.environ['BOT_TOKEN']
HEROKU_APP_URL = os.environ['HEROKU_APP_URL']

server = Flask(__name__)
bot = telebot.AsyncTeleBot(BOT_TOKEN)

help_cmd_message = ''' Сәлем, {0},
 Маған кириллицамен қазақша жазсаң, мен саған оны латын графикасына аударып берем.\n
Привет, {0},
 Просто напиши мне на казахском на кириллице, и Я переведу твой текст на латинскую графику.\n
Contacts: Telephon number: 87073441069, e-mail: rsshyngys@gmail.com
                   '''               

def transliterate(text):
    letters_mapping = {
        "а":"a", "ә":"á", "б":"b", "в":"v", "д":"d", "е":"e", "ф":"f",
        "г":"g", "ғ":"ǵ", "х":"h", "һ":"h", "і":"i", "и":"ı", "й":"ı",
        "ж":"j", "к":"k", "л":"l", "м":"m", "н":"n", "ң":"ń", "о":"o",
        "ө":"ó", "п":"p", "қ":"q", "р":"r", "с":"s", "ш":"sh", "ч":"ch",
        "т":"t", "ұ":"u", "ү":"ú", "ы":"y", "у":"ý", "з":"z",
        
        "А":"A", "Ә":"Á", "Б":"B", "В":"V", "Д":"D", "Е":"E", "Ф":"F",
        "Г":"G", "Ғ":"Ǵ", "Х":"H", "Һ":"H", "І":"I", "И":"I", "Й":"I",
        "Ж":"J", "К":"K", "Л":"L", "М":"M", "Н":"N", "Ң":"Ń", "О":"O",
        "Ө":"Ó", "П":"P", "Қ":"Q", "Р":"R", "С":"S", "Ш":"Sh", "Ч":"Ch",
        "Т":"T", "Ұ":"U", "Ү":"Ú", "Ы":"Y", "У":"Ý", "З":"Z"    
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

@bot.message_handler(commands=["start", "help"])
def help_cmd_handler(message):
    print(message.from_user.first_name, message.from_user.username, message.chat.id, message.chat.type, message.text)
    bot.send_message(message.chat.id, help_cmd_message.format(message.from_user.first_name)).wait()
    
@bot.message_handler(content_types=["text"])
def send_transliterated(message):
    #print(message.from_user.first_name, message.from_user.username, message.chat.id, message.chat.type, message.text)
    print(message)
    print("length = ", len(message.text))
    bot.reply_to(message, transliterate(message.text)).wait()       
    
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
