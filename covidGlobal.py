import json
import requests
import unicodedata
import re
import locale
import flag

from constants import globalCovidUrl,globalCovidCountry
from util import JsonToObject, getLocale

def makeRequest(lugar):
    query = "countries/" + lugar
    return requests.get(globalCovidUrl+query).json()

def requestAll():
    return requests.get(globalCovidCountry).json()

def globalCovid(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    response = JsonToObject(text)
    try:
        formatado = "Casos: {suspect}\nCasos Ativos: {cases}\nRecuperados: {recovered}\nMortes: {deaths}\nCasos descobertos hoje: {today}\nMortes Hoje: {deathsToday}".format(
            cases=locale.format_string('%d', response.active,1), suspect=locale.format_string('%d', response.cases,1), deaths=locale.format_string('%d',response.deaths,1), recovered=locale.format_string('%d', response.recovered,1),today=locale.format_string('%d', response.todayCases,1), deathsToday=locale.format_string('%d', response.todayDeaths,1))
        return response.countryInfo['flag'], formatado
    except:
        pass
