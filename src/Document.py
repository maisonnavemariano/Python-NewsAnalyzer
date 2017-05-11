import re
import enchant
import pickle


# re.sub(r"'(.*)'", "\g<1>", "what 'ever' you want")   eliminar comillas simples, dejar lo que esta adentro.

PATTERN_COMILLAS = "\'[^\ ]*"
PATTERN_SEPARADORES = "[\.\,\:\;\?\!]"
PATTERN_CHAR_ESPECIALES = "[^\ ]*[^a-zA-Z\ ][^\ ]*"
PATTERN_MULT_BLANKS = " +"
PATTERN_BETWEEN_QUOTES = "'([^\ ])'"
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




def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class Document(object):

    #location2code = pickle.load(open("../db/pickle/map_location2code.p","rb"))
    country2code = pickle.load(open("../db/pickle/map_country2code.p","rb"))

    def __init__(self, title,sectionName = "", date="", instanceNro=-1):
        self.instanceNro = instanceNro
        self.sectionName = sectionName.replace(" ","")
        self.words = {}
        self.date = date
        self.title = self._prefilterText(title)
        self.locations = set()
        self._bodyText = ""



    def setOriginalText(self,originalText):
        self._bodyText = cleanhtml(originalText).lower()
    def obtenerTextoOriginal(self):
        return self._bodyText

    def _prefilterText(self,text):
        text = cleanhtml(text)
        text = re.sub(PATTERN_BETWEEN_QUOTES, "\g<1>", text)
        text = re.sub(PATTERN_COMILLAS, "",text)
        text = re.sub(PATTERN_SEPARADORES," ",text)
        text = re.sub(PATTERN_CHAR_ESPECIALES, "",text)
        text = re.sub(PATTERN_MULT_BLANKS, " ",text)
        text = text.lower()
        return text
    def addText(self, text, stopwords):
        text = self._prefilterText(text)
        #text = "".join(c for c in text if c in self.PERMITTED_CHARS)
        # for location in self.location2code:
        #     if location in text:
        #         self.locations.add(location)
        for country in self.country2code:
            if country in text:
                self.locations.add(country)
        words_array = text.split(" ")
        for word in words_array:
            if not word in stopwords and len(word) > 0:
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



def combinarDocumentos(lista_documentos,nombreDelConjunto  ):
    nuevoDocumento = Document(nombreDelConjunto)
    palabras = {}
    for documento in lista_documentos:
        for palabra in documento.words:
            if not palabra in palabras:
                palabras[palabra] = documento.words[palabra]
            else:
                palabras[palabra] = palabras[palabra] + documento.words[palabra]
    return nuevoDocumento