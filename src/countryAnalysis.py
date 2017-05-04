#!/usr/bin/python3
import readDocuments
import tfidf
import numpy
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

INPUT = "../db/noticias/enero"
def sortByRelevance():
# Obtenemos TODOS los documentos.
    stopwords_files, ignored_words_file,selected_country = initVar()
    stopwords_files.append(ignored_words_file)
    documentos = readDocuments.getDocuments(INPUT, stopwords_files)

    # nos quedamos con los documentos que hablen de $selected_country
    documentosDelPais = [document for document in documentos if selected_country in document.locations]

    _, matriz_tfidf = tfidf.createTFIDF(list_documents=documentosDelPais)

    #Creamos matrix similitud
    matrixSimilaridad = tfidf.createSimilarityMatrix(matriz_tfidf)

    list_and_relevance = []
    docNro = 0
    for doc in documentosDelPais:
        f1 = funcionImportanciaNoticiaPais(doc,selected_country)
        f2 = funcionImportanciaNoticiaEnDataset(docNro,matrixSimilaridad)
        list_and_relevance.append( (f1*f2,doc ) )
        docNro = docNro + 1

    return sorted(list_and_relevance)




def funcionImportanciaNoticiaPais(document, pais):
    if pais in document.title:
        return 1.0
    else:
        if pais not in document.obtenerTextoOriginal():
            return 0.0
        else:
            primeraAparicion = document.obtenerTextoOriginal().find(pais)
            valor =  primeraAparicion/len(document.obtenerTextoOriginal())
            if document.obtenerTextoOriginal().count(pais) > 1:
                valor = valor * 1.1
            return valor


def funcionImportanciaNoticiaEnDataset(indiceNoticia, matrizSimilaridad):
    _,columncount = matrizSimilaridad.shape
    return (sum(matrizSimilaridad[indiceNoticia])-1)/columncount

