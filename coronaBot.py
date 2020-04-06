import telepot
import telepot.api
import json
import requests
import unicodedata
import re
import flag
import urllib.request
from random import randint
from operator import itemgetter

bot = telepot.Bot('')

class JsonToObject(object):
    def __init__(self, data):
	    self.__dict__ = json.loads(data)
	    
def makeRequest(lugar):
    return requests.get("https://corona.lmao.ninja/countries/"+lugar).json()

def requestAll():
    return requests.get("https://corona.lmao.ninja/countries/").json()

def globalCovid(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    response = JsonToObject(text)
    try:
        formatado = "Casos: {suspect}\nCasos Ativos: {cases}\nRecuperados: {recovered}\nMortes: {deaths}\nCasos descobertos hoje: {today}\nMortes Hoje: {deathsToday}".format(cases=response.active, suspect=response.cases, deaths=response.deaths, recovered=response.recovered, today=response.todayCases, deathsToday= response.todayDeaths)
        return response.countryInfo['flag'], formatado
    except: pass

def brazilCovid():
    openzada = urllib.request.urlopen("https://sigageomarketing.com.br/coronavirus/coronavirus.js")
    s = openzada.read().decode('utf-8').replace("var dados = ", "")
    final = JsonToObject(s)
    return final.features

def searchCountry(lugar):
    obj = brazilCovid()
    for index in range(len(obj)):
        searchedCountry = removerAcentosECaracteresEspeciais(obj[index]['properties']['estado_geo'])
        toSearch = removerAcentosECaracteresEspeciais(lugar)
        splitted = searchedCountry.split(" ")
        splittedSize = len(splitted)
        if len(splitted) > 1:
            joined = " ".join(splitted[0:splittedSize-1]).lower()
            if toSearch.lower() == joined or toSearch.lower() == splitted[splittedSize-1].lower():
                response = obj[index]['properties']
                estadoSplitado = response["estado_geo"].split(" ")
                estado = " ".join(estadoSplitado[0:len(estadoSplitado)-1]).lower()
                return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=int(response['casosconfirmados']), deaths=response['obitos']), estado
            
        if(toSearch.title() in searchedCountry):
            response = obj[index]['properties']
            return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=int(response['casosconfirmados']), deaths=response['obitos'])
    
def removerAcentosECaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def getFlag(province):
    if province in ["sao paulo","são paulo", "São Paulo", "São paulo"]:
        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}1-300x200.png?x64851".format(provinceName=province.replace(" ","-").lower())
    else:

        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x210.png?x64851".format(provinceName=province.replace(" ","-").lower())
    #return "https://www.enemvirtual.com.br/uploadedfiles/uploads/2011/07/bandeira_{provinceName}.gif".format(provinceName=province.replace(" ","_"))

def getOtherFlag(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x200.png?x64851".format(provinceName=province.replace(" ","-").lower())
def getOtherFlag2(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x214.png?x64851".format(provinceName=province.replace(" ","-").lower())

def hasShouth(obj):
    if "south" in obj:
        teste = obj.split(" ")
        teste = "s.%20"+teste[1]
        return teste
    if obj.find(" "):
        return obj.replace(" ", "%20")
    return obj
    
def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg['from']['username']
    userid = msg['from']['id']
    rpli = msg['message_id']
    user = msg['from']['username']
    id = msg['from']['id']
    notRecognized = "Oops! Nothing found about, try another country c:"

    if content_type == 'text':
        received = re.sub("\s\s+", " ",msg['text'].strip())
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
                bot.sendPhoto(chat_id, send[0], caption= send[1])
            except:
                bot.sendMessage(chat_id, notRecognized)
                
        if splittedMsg[0] == "/covidbr":
            country = " ".join(splittedMsg[1:])
            #flag = getFlag(removerAcentosECaracteresEspeciais(country))
            response = searchCountry(country)
            if response:
                try:
                    bot.sendPhoto(chat_id, getFlag(removerAcentosECaracteresEspeciais(response[1])), caption=response[0])
                except:
                    bot.sendPhoto(chat_id, getOtherFlag(removerAcentosECaracteresEspeciais(response[1])), caption=response[0])
                else:
                        bot.sendPhoto(chat_id, getOtherFlag2(removerAcentosECaracteresEspeciais(response[1])), caption=response[0])
            else:
                bot.sendMessage(chat_id, notRecognized)

        if splittedMsg[0] == "/r":
            newlist = []
            final = "\n"
            if splittedMsg[1].find("-"):
                newlist = sorted(requestAll(), key=itemgetter('cases'), reverse=True)
                cinco = newlist[:abs(int(splittedMsg[1]))]
                for i in cinco:
                    if i["countryInfo"]["iso2"]:
                        final += flag.flag(i["countryInfo"]["iso2"]) + " " +str(i["country"]) +":  "+ str(i["cases"]) + "\n"
                    else:
                        final += "NA " +str(i["country"]) +":  "+ str(i["cases"]) + "\n"
                    
            else:
                newlist = sorted(requestAll(), key=itemgetter('cases'), reverse=False)
                cinco = newlist[:abs(int(splittedMsg[1]))]
                for i in cinco:
                    if i["countryInfo"]["iso2"]:
                        final += flag.flag(i["countryInfo"]["iso2"]) + " " + str(i["country"]) +":  "+ str(i["cases"]) + "\n"
                    else:
                        final +=  "NA " + str(i["country"]) +":  "+ str(i["cases"]) + "\n"
               

            bot.sendMessage(chat_id, "*Covid 19 cases raking per country*"+final, parse_mode='Markdown')

bot.message_loop(handle)
