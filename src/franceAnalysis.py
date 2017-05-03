#!/usr/bin/python3
from readDocuments import getDocuments
from tfidf import createTFIDF
from Clustering import applyClustering
from Clustering import getClusters
from Clustering import saveResult
CONFIG = "../etc/var.config"
def initVar():
    SVD_ANALYSIS = "SVD_ANALYSIS = "
    IGNORED_COEFFICIENTS = "IGNORED_COEFFICIENTS = "
    STOPWORD_FILES = "STOPWORDS_FILES = "
    IGNORED_WORDS_FILE = "IGNORED_WORDS_FILE = "
    CON_FECHA = "WITH_DATE = "
    SAVE_ARFF = "SAVE_ARFF = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(STOPWORD_FILES):
                stopwords = line[len(STOPWORD_FILES)+2:-3].split('\",\"')
            if line.startswith(IGNORED_WORDS_FILE):
                ignored_words_file = line[len(IGNORED_WORDS_FILE)+1:-2]


    return stopwords, ignored_words_file



INPUT = "../db/noticias/enero"


stopwords_list,ignored_words_file = initVar()
stopwords_list.append(ignored_words_file)
todo_los_documentos = getDocuments(INPUT, stopwords_list)

documentos_sobre_francia = []
for document in todo_los_documentos:
    if "mali" in document.locations:
        documentos_sobre_francia.append(document)

print("cantidad de documentos con los que trabajar: "+str(len(documentos_sobre_francia)))
documentos, matriz = createTFIDF(  list_documents=documentos_sobre_francia)
documentosEtiquetados,centroides = applyClustering(matriz,documentos)
clusters = getClusters(documentosEtiquetados)
#Guardar resultados.
saveResult(documentosEtiquetados,clusters)
