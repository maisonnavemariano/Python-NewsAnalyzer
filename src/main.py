from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
INPUT = "../db/noticias/enero"
STOPWORDS_FILES = ["../stopwords/SmartStoplist.txt","../stopwords/stopword1.txt","../stopwords/stopword2.txt","../stopwords/stopword3.txt"]
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"

# Optional 1 - recalcular palabras ignoradas (frecuencia 1)
threshold = 3
computeIgnoredWords(threshold, INPUT,IGNORED_WORDS_FILE,STOPWORDS_FILES) #primero usamos los stop words sin palabras ignoradas (para la generacion)

#Crear tf-idf
SVD_ANALYSIS = True
IGNORED_COEFFICIENTS = 20
dataset_filtrado = False
STOPWORDS_FILES.append(IGNORED_WORDS_FILE)
createTFIDF(INPUT, dataset_filtrado, STOPWORDS_FILES, SVD_ANALYSIS ,IGNORED_COEFFICIENTS ) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas