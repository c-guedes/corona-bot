import telepot
import telepot.api
import json
import requests
from random import randint

bot = telepot.Bot('KEY_HERE')


def makeRequest(lugar):
    return requests.get("https://corona.lmao.ninja/countries/"+lugar+"?strict=true").json()


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    response = ResponseCase(text)
    formatado = "Casos Total: {cases}\nCasos Suspeitos: {suspect}\nMortes: {deaths}\nRecuperados: {recovered}\nCasos descobertos hoje: {today}\nMortes Hoje: {deathsToday}".format(cases=response.active, suspect=response.cases, deaths=response.deaths, recovered=response.recovered, today=response.todayCases, deathsToday= response.todayDeaths)
    return response.countryInfo['flag'], formatado


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg['from']['username']
    userid = msg['from']['id']
    rpli = msg['message_id']
    user = msg['from']['username']
    id = msg['from']['id']

    if content_type == 'text':
        if "/covid" in msg['text']:
            repl = msg['text'].split(' ')
            country = repl[1]
            send = jprint(makeRequest(country))
            bot.sendPhoto(chat_id, send[0], caption= send[1])


bot.message_loop(handle)

class ResponseCase(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)
