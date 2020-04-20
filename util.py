import locale
import unicodedata
import re
import json
from random import randint
from operator import itemgetter

locale.setlocale(locale.LC_ALL, '') #pega o local da máquina e seta o locale

class JsonToObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)

def removeTypo(palavra):
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join(
        [c for c in nfkd if not unicodedata.combining(c)])
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento)

def hasShouth(obj):
    if "south" in obj:
        teste = obj.split(" ")
        teste = "s.%20"+teste[1]
        return teste
    if obj.find(" "):
        return obj.replace(" ", "%20")
    return obj

def getLocale():
    locale.setlocale(locale.LC_ALL, '')