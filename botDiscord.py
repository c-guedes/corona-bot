import discord
import json,flag
import requests
import urllib.request
import unicodedata
import re
from discord.ext import commands
from operator import itemgetter
import time

token = ""


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
        formatado = "Casos: {suspect}\nCasos Ativos: {cases}\nRecuperados: {recovered}\nMortes: {deaths}\nCasos descobertos hoje: {today}\nMortes Hoje: {deathsToday}".format(
            cases=response.active, suspect=response.cases, deaths=response.deaths, recovered=response.recovered, today=response.todayCases, deathsToday=response.todayDeaths)
        return response.countryInfo['flag'], formatado
    except:
        pass


def brazilCovid():
    openzada = urllib.request.urlopen(
        "https://sigageomarketing.com.br/coronavirus/coronavirus.js")
    s = openzada.read().decode('utf-8').replace("var dados = ", "")
    final = JsonToObject(s)
    return final.features


def searchCountry(lugar):
    obj = brazilCovid()
    for index in range(len(obj)):
        searchedCountry = removerAcentosECaracteresEspeciais(
            obj[index]['properties']['estado_geo'])
        toSearch = removerAcentosECaracteresEspeciais(lugar)
        splitted = searchedCountry.split(" ")
        splittedSize = len(splitted)
        if len(splitted) > 1:
            joined = " ".join(splitted[0:splittedSize-1]).lower()
            if toSearch.lower() == joined or toSearch.lower() == splitted[splittedSize-1].lower():
                response = obj[index]['properties']
                estadoSplitado = response["estado_geo"].split(" ")
                estado = " ".join(
                    estadoSplitado[0:len(estadoSplitado)-1]).lower()
                return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=int(response['casosconfirmados']), deaths=response['obitos']), estado

        if(toSearch.title() in searchedCountry):
            response = obj[index]['properties']
            return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=int(response['casosconfirmados']), deaths=response['obitos'])


def removerAcentosECaracteresEspeciais(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join(
        [c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)


def getFlag(province):
    if province in ["sao paulo", "são paulo", "São Paulo", "São paulo"]:
        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}1-300x200.png?x64851".format(provinceName=province.replace(" ", "-").lower())
    else:

        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x210.png?x64851".format(provinceName=province.replace(" ", "-").lower())
    # return "https://www.enemvirtual.com.br/uploadedfiles/uploads/2011/07/bandeira_{provinceName}.gif".format(provinceName=province.replace(" ","_"))


def getOtherFlag(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x200.png?x64851".format(provinceName=province.replace(" ", "-").lower())


def getOtherFlag2(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x214.png?x64851".format(provinceName=province.replace(" ", "-").lower())


def hasShouth(obj):
    if "south" in obj:
        teste = obj.split(" ")
        teste = "s.%20"+teste[1]
        return teste
    if obj.find(" "):
        return obj.replace(" ", "%20")
    return obj


client = commands.Bot(command_prefix="-")
client.remove_command("help")

@client.event
async def on_ready():
    print("Running")


@client.command()
async def covid(ctx, *, args):
    country = hasShouth(args)
    send = globalCovid(makeRequest(country))
    notRecognized = "Oops! Nothing found about it, try another country c:"

    try:
        await ctx.send(send[1])
    except:
        await ctx.send(notRecognized)
        
    
@client.command()
async def covidbr(ctx, *, args):
    response = searchCountry(args)
    notRecognized = "Oops! Nothing found about it, try another country c:"
    try:
        await ctx.send(response[0])
    except:
        await ctx.send(notRecognized)
    
# @client.event
# async def on_message(message):    
#     if message.content.startswith("-help"):
#         embed = discord.Embed(
#             colour = discord.Colour.orange()
#         )
#         print(message.author)
#         embed.set_author(name="help")
#         embed.add_field(name="-covid country", value="Returns global covid cases", inline= True)
#         embed.add_field(name="-covidbr country", value="Returns Brazil cases", inline= True)
        
#         await client.send_message(message.author, embed=embed)

@client.command()
async def r(ctx, arg):
    newlist = []
    final = "\n"
    if arg.find("-"):
        newlist = sorted(
            requestAll(), key=itemgetter('cases'), reverse=True)
        cinco = newlist[:abs(int(splittedMsg[1]))]
        for i in cinco:
            if i["countryInfo"]["iso2"]:
                final += flag.flag(i["countryInfo"]["iso2"]) + " " + \
                    str(i["country"]) + ":  " + str(i["cases"]) + "\n"
            else:
                final += "NA " + \
                    str(i["country"]) + ":  " + str(i["cases"]) + "\n"

    else:
        newlist = sorted(requestAll(), key=itemgetter(
            'cases'), reverse=False)
        cinco = newlist[:abs(int(splittedMsg[1]))]
        for i in cinco:
            if i["countryInfo"]["iso2"]:
                final += flag.flag(i["countryInfo"]["iso2"]) + " " + \
                    str(i["country"]) + ":  " + str(i["cases"]) + "\n"
            else:
                final += "NA " + \
                    str(i["country"]) + ":  " + str(i["cases"]) + "\n"

    ctx.send( "*Covid 19 cases ranking per country*"+final, parse_mode='Markdown')
            
client.run(token)
