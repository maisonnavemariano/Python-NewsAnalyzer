#!/usr/bin/python3
from dictionaryAnalyze import DiccionarioPalabras
import readDocuments
import tfidf
import numpy
from pathlib import Path
import pickle
from dictionaryAnalyze import DiccionarioPalabras

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

    dic = DiccionarioPalabras()
    ec = 0
    not_ec = 0
    for doc in documentos:
        if dic.isEconomic(doc):
            ec +=1
        else:
            not_ec+=1
    print("documentos no economicos: {0}. Vs documentos economicos: {1}.".format(str(not_ec),str(ec)))

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
    funcImportanciaPais = []

    diccionario_economico = DiccionarioPalabras()
    func_relevancia_economica = diccionario_economico.funcEconomicRelevance(documentosDelPais)

    for doc in documentosDelPais:
        f1 = funcionImportanciaNoticiaPais(doc,selected_country)
        funcImportanciaPais.append(f1)
        #print("f1: "+str(f1))


    docNro = 0
    factor_ajuste_importancia_en_pais = 2.0
    factor_ajuste_importancia_economia = 1.0
    factor_ajuste_importancia_en_dataset = 1
    for doc in documentosDelPais:
        f2 = funcionImportanciaNoticiaEnDataset(docNro,matrixSimilaridad,funcImportanciaPais)
        #print("f2: "+str(f2))
        relevancia = factor_ajuste_importancia_en_pais * funcImportanciaPais[docNro]
        relevancia *= factor_ajuste_importancia_economia * func_relevancia_economica[docNro]
        relevancia *= factor_ajuste_importancia_en_dataset * f2
        list_and_relevance.append( [doc, relevancia] )
        docNro += 1

    list_and_relevance.sort(key=lambda x: x[1], reverse=True)
    return list_and_relevance




def funcionImportanciaNoticiaPais(document, pais):
    if pais not in document.obtenerTextoOriginal().lower():
        return 0.0
    else:
        primeraAparicion = len(document.obtenerTextoOriginal()) - document.obtenerTextoOriginal().find(pais)
        valor =  float(primeraAparicion)/float(len(document.obtenerTextoOriginal()))
        if document.obtenerTextoOriginal().count(pais) > 1:
            valor = valor + 0.1
        if pais in document.title.lower():
            valor = valor + 0.5
        if len(document.locations) > 2:
            valor = valor - 0.1
        return valor/1.6


def funcionImportanciaNoticiaEnDataset(indiceNoticia, matrizSimilaridad,funcImportanciaPais):
   # max = numpy.amax([sum(x) for x in matrizSimilaridad])
    _,columncount = matrizSimilaridad.shape
    suma = 0.0
    doc_j = 0
    for elem in matrizSimilaridad[indiceNoticia]:
        if elem > 0.2 and not doc_j==indiceNoticia:
            suma = suma +  elem * funcImportanciaPais[doc_j]
        doc_j+=1
    return (suma) / (len(matrizSimilaridad[indiceNoticia])-1)



