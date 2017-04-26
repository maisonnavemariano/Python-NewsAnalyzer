from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
from Clustering import applyClustering
from LabeledDocument import LabeledDocument
INPUT = "../db/noticias/enero"
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"

# Optional 1 - recalcular palabras ignoradas (frecuencia 1)

computeIgnoredWords( INPUT,IGNORED_WORDS_FILE) #primero usamos los stop words sin palabras ignoradas (para la generacion)

#Crear tf-idf
dataset_filtrado = False
documentos, matriz  = createTFIDF(INPUT, dataset_filtrado ) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas

documentosEtiquetados = applyClustering(matriz,documentos)

writer = open("../db/resultados/clusters.txt", "w")
for doc in documentosEtiquetados:
    writer.write(doc.document.title+",cluster"+str(doc.label)+"\n")
writer.close()