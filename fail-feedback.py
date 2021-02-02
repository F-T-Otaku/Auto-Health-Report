import sys
import time
import telebot

output = "体温上报失败" + "\n\n"
SCKEY = sys.argv[1]
TOKEN = sys.argv[2]
CHAT_ID = sys.argv[3]
serverChan = f"https://sc.ftqq.com/{SCKEY}.send"
bot = telebot.TeleBot(TOKEN)
timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
output = output + "[" + timestamp + "]report failed"
requests.post(ServerChan, data={'text': '体温填写情况', 'desp': output})
bot.send_message(CHAT_ID, output)
