import telepot,telepot.api,json,requests,locale,flag, re
import urllib.request
from operator import itemgetter
import time

from constants import botKey
from util import hasShouth,removeTypo
from covidGlobal import requestAll, makeRequest, globalCovid
from covidBrasil import brazilCovid, searchCountry, getFlag, getOtherFlag, getOtherFlag2, somatoria

locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

bot = telepot.Bot(botKey)

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg['from']['username']
    userid = msg['from']['id']
    rpli = msg['message_id']
    user = msg['from']['username']
    id = msg['from']['id']
    notRecognized = "Oops! Nothing found about, try another country c:"

    if content_type == 'text':
        received = re.sub("\s\s+", " ", msg['text'].strip())
        splittedMsg = received.split(' ')
        if received == "/help":
            send = "/covid country - for global covid\n/covidbr state - for brazilian states\n/r number - to rank countries"
            bot.sendMessage(chat_id, send)

        if received == "/help@corona4allbot":
            send = "/covid country - for global covid\n/covidbr state - for brazilian states\n/r number - to rank countries"
            bot.sendMessage(chat_id, send)

        if received == "/start":
            send = "Hey there! Simple bot to check covid status, any typo or error could message me @gueedes\n\n/covid country - for global covid\n/covidbr state - for brazilian states"
            bot.sendMessage(chat_id, send)

        if splittedMsg[0] == "/covid":
            repl = received.split(' ')
            country = hasShouth(" ".join(repl[1:]))
            send = globalCovid(makeRequest(country))
            try:
                bot.sendPhoto(chat_id, send[0], caption=send[1])
            except:
                bot.sendMessage(chat_id, notRecognized)

        if splittedMsg[0] == "/covidbr":
            country = " ".join(splittedMsg[1:])
            response = searchCountry(country)
            if response:
                try:
                    bot.sendPhoto(chat_id, getFlag(
                        removeTypo(response[1])), caption=response[0])
                except:
                    bot.sendPhoto(chat_id, getOtherFlag(
                        removeTypo(response[1])), caption=response[0])
                else:
                    bot.sendPhoto(chat_id, getOtherFlag2(
                        removeTypo(response[1])), caption=response[0])
            else:
                bot.sendMessage(chat_id, notRecognized)

        if splittedMsg[0] == "/brasil":
            bot.sendMessage(chat_id, somatoria())
            
        if splittedMsg[0] == "/r":
            newlist = []
            final = "\n"
            if splittedMsg[1].find("-"):
                newlist = sorted(
                    requestAll(), key=itemgetter('cases'), reverse=True)
                cinco = newlist[:abs(int(splittedMsg[1]))]
                for i in cinco:
                    if i["countryInfo"]["iso2"]:
                        final += flag.flag(i["countryInfo"]["iso2"]) + " " + \
                            str(i["country"]) + ":  " + str(locale.format_string('%d', int(i["cases"]), 1)) + "\n"
                    else:
                        final += "NA " + \
                            str(i["country"]) + ":  " + str(locale.format_string('%d', int(i["cases"]), 1)) + "\n"

            else:
                newlist = sorted(requestAll(), key=itemgetter(
                    'cases'), reverse=False)
                cinco = newlist[:abs(int(splittedMsg[1]))]
                for i in cinco:
                    if i["countryInfo"]["iso2"]:
                        final += flag.flag(i["countryInfo"]["iso2"]) + " " + \
                            str(i["country"]) + ":  " + str(locale.format_string('%d', int(i["cases"]), 1))+ "\n"
                    else:
                        final += "NA " + \
                            str(i["country"]) + ":  " + str(locale.format_string('%d', int(i["cases"]), 1)) + "\n"

            bot.sendMessage(
                chat_id, "*Covid 19 cases ranking per country*"+final, parse_mode='Markdown')


bot.message_loop(handle)
print("Running")
while 1:
   time.sleep(2000)
