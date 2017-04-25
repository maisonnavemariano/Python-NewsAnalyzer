import re
import enchant
from lib.yahooAPI import validPlace
d = enchant.Dict("en_UK")
CONFIG = "../etc/var.config"



def initVar():
    FACTOR_POND = "FACTOR_PONDERACION = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(FACTOR_POND):
                factor_pond = int(line[len(FACTOR_POND):-1])
    return factor_pond


factor_ponderacion = initVar()
from nltk.stem import RegexpStemmer
from nltk.stem import LancasterStemmer
st_regex = RegexpStemmer('ing$|s$|e$|able$', min=4)
st_lancaster = LancasterStemmer()
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Document(object):
    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def __init__(self, title,sectionName = "", date=""):
        self.sectionName = sectionName.replace(" ","")
        self.words = {}
        self.date = date
        self.title = "".join(c for c in title if c in self.PERMITTED_CHARS)

    def hasInvalidCharacter(self, cadena):
        return len("".join(c for c in cadena if c in self.PERMITTED_CHARS))< len(cadena)


    def addText(self, text, stopwords):
        text = text.lower()
        text = cleanhtml(text)
        #text = "".join(c for c in text if c in self.PERMITTED_CHARS)
        words_array = text.split(" ")
        for word in words_array:
            if not word in stopwords and len(word) > 0 and not hasNumbers(word) and not self.hasInvalidCharacter(word):
                frecuencia =  1
                stem_word_regex = st_regex.stem(word)
                stem_word_lancaster = st_lancaster.stem(word)
                if d.check(stem_word_lancaster):
                    word = stem_word_lancaster
                else:
                    if d.check(stem_word_regex):
                        word = stem_word_regex
                if (not d.check(word)):
                    frecuencia = frecuencia * factor_ponderacion
                if word in self.words :
                    self.words[word] = self.words[word] + frecuencia
                else:
                    self.words[word] = frecuencia

