import requests
import unicodedata
import re
import locale
import flag
import urllib.request
from operator import itemgetter

from util import JsonToObject, removeTypo
from constants import brazilCovidUrl

locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

def brazilCovid():
    openzada = urllib.request.urlopen(brazilCovidUrl)
    s = openzada.read().decode('utf-8').replace("var dados =", "")
    final = JsonToObject(s)
    return final.features

def somatoria():
    obj = brazilCovid()
    objBr = obj[len(obj)-1]['properties']
    return "Casos confirmados: {confirmedCases}\nObitos: {deaths}".format(confirmedCases= locale.format_string('%d', int(objBr['casosconfirmados']),1), deaths = locale.format_string('%d', int(objBr['obitos']),1))

def searchCountry(lugar):
    obj = brazilCovid()
    for index in range(len(obj)):
        print(index)
        searchedCountry = removeTypo(
            obj[index]['properties']['estado_geo'])
        toSearch = removeTypo(lugar)
        splitted = searchedCountry.split(" ")
        splittedSize = len(splitted)
        if len(splitted) > 1:
            joined = " ".join(splitted[0:splittedSize-1]).lower()
            if toSearch.lower() == joined or toSearch.lower() == splitted[splittedSize-1].lower():
                response = obj[index]['properties']
                estadoSplitado = response["estado_geo"].split(" ")
                estado = " ".join(
                    estadoSplitado[0:len(estadoSplitado)-1]).lower()
                return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=locale.format_string('%d', int(response['casosconfirmados']),1), deaths=locale.format_string('%d', response['obitos'],1)), estado

        if(toSearch.title() in searchedCountry):
            response = obj[index]['properties']
            return "Casos Confirmados: {confirmedCases}\nMortes: {deaths}".format(confirmedCases=locale.format_string('%d', int(response['casosconfirmados']),1), deaths=locale.format_string('%d', response['obitos'],1)   )


def getFlag(province):
    if province in ["sao paulo", "são paulo", "São Paulo", "São paulo"]:
        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}1-300x200.png?x64851".format(provinceName=province.replace(" ", "-").lower())
    else:
        return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x210.png?x64851".format(provinceName=province.replace(" ", "-").lower())


def getOtherFlag(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x200.png?x64851".format(provinceName=province.replace(" ", "-").lower())


def getOtherFlag2(province):
    return"https://www.estadosecapitaisdobrasil.com/wp-content/uploads/2014/09/bandeira-{provinceName}-300x214.png?x64851".format(provinceName=province.replace(" ", "-").lower())
