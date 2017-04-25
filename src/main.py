from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
INPUT = "../db/noticias/enero"
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"

# Optional 1 - recalcular palabras ignoradas (frecuencia 1)

computeIgnoredWords( INPUT,IGNORED_WORDS_FILE) #primero usamos los stop words sin palabras ignoradas (para la generacion)

#Crear tf-idf
dataset_filtrado = False
createTFIDF(INPUT, dataset_filtrado ) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas