#!/usr/bin/python3
import readDocuments
import tfidf
import numpy
from pathlib import Path
import pickle

########################################################################
#
# Pasos:
#   1. Levantar los documentos. Sabiendo de cada uno de ellos:
#                                                               * titulo
#                                                               * fecha (epoch)
#                                                               * ubicaciones
#                                                               * texto original
#                                                               * mapeo palabra a frec.
#
#   2. Generar conjunto de documentos que tienen como ubicacion el país INPUT
#   3. Aplicar tf-idf sobre el conjunto de documentos.
#   4. Obtener matriz similitud entre documentos multiplicando matrix por inversa transpuesta.
#   5. Clustering ?
#
#
########################################################################

# * * * * * * Leemos la configuración de la ejecución * * * * * * * * * *
CONFIG = "../etc/var.config"
def initVar():
    stopwords_file_const = "STOPWORDS_FILES = "
    ignored_word_const = "IGNORED_WORDS_FILE = "
    selected_country_const = "SELECTED_COUNTRY = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(stopwords_file_const):
                stopwords = line[len(stopwords_file_const) + 2:-3].split('\",\"')
            if line.startswith(ignored_word_const):
                ignored_words_file = line[len(ignored_word_const)+1:-2]
            if line.startswith(selected_country_const):
                selected_country = line[len(selected_country_const):-1]
    return stopwords,ignored_words_file,selected_country
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

INPUT = "../db/noticias/noticias2013"
OUTPUT_DOCS = Path("../db/pickle/todos_los_documentos.p")
def sortByRelevance():
# Obtenemos TODOS los documentos.

    stopwords_files, ignored_words_file,selected_country = initVar()
    stopwords_files.append(ignored_words_file)
    if not OUTPUT_DOCS.is_file():
        documentos = readDocuments.getDocuments(INPUT, stopwords_files)
        pickle.dump(documentos, open(str(OUTPUT_DOCS),"wb") )
    else:
        documentos = pickle.load(open(str(OUTPUT_DOCS),"rb"))

    # nos quedamos con los documentos que hablen de $selected_country
    documentosDelPais = [document for document in documentos if selected_country in document.locations]
    print("Cantidad de documentos que hablan del país: "+str(len(documentosDelPais)))

    _, matriz_tfidf,lista_palabras = tfidf.createTFIDF(list_documents=documentosDelPais)
    # writer = open("tmp.txt","w")
    # line = ""
    # for palabra in lista_palabras:
    #     line = line + palabra+ " "
    # writer.write(line[:-1]+"\n")
    # for row in matriz_tfidf:
    #     line = ""
    #     for element in row:
    #         line = line + str(element)+" "
    #     writer.write(line[:-1]+"\n")
    # writer.close()

    #print(matriz_tfidf)
    #Creamos matrix similitud
    matrixSimilaridad = tfidf.createSimilarityMatrix(matriz_tfidf)

    list_and_relevance = []
    docNro = 0
    for doc in documentosDelPais:
        f1 = funcionImportanciaNoticiaPais(doc,selected_country)
        #print("f1: "+str(f1))
        f2 = funcionImportanciaNoticiaEnDataset(docNro,matrixSimilaridad)
        #print("f2: "+str(f2))
        list_and_relevance.append( [doc, f1*f2 ] )
        docNro = docNro + 1


    list_and_relevance.sort(key=lambda x: x[1], reverse=True)
    return list_and_relevance




def funcionImportanciaNoticiaPais(document, pais):
    if pais not in document.obtenerTextoOriginal().lower():
        return 0.0
    else:
        primeraAparicion = len(document.obtenerTextoOriginal()) - document.obtenerTextoOriginal().find(pais)
        valor =  float(primeraAparicion)/float(len(document.obtenerTextoOriginal()))
        if document.obtenerTextoOriginal().count(pais) > 1:
            valor = valor * 1.1
        if pais in document.title.lower():
            valor = valor * 1.5
        return valor


def funcionImportanciaNoticiaEnDataset(indiceNoticia, matrizSimilaridad):
    _,columncount = matrizSimilaridad.shape
    return (sum(matrizSimilaridad[indiceNoticia])-1)/float(columncount)

