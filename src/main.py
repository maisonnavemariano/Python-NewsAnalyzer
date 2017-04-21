from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
INPUT = "../db/noticias/enero"
STOPWORDS_FILES = ["../stopwords/SmartStoplist.txt"]
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"

# Optional 1 - recalcular palabras ignoradas (frecuencia 1)
threshold = 3
computeIgnoredWords(threshold, INPUT,IGNORED_WORDS_FILE,STOPWORDS_FILES) #primero usamos los stop words sin palabras ignoradas (para la generacion)

#Crear tf-idf
dataset_filtrado = False
STOPWORDS_FILES.append(IGNORED_WORDS_FILE)
createTFIDF(INPUT, dataset_filtrado, STOPWORDS_FILES) # luego como stop words usamos las listas anteriores y las de palabras ignoradas

