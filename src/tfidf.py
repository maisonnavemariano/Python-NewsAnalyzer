#!/usr/bin/python3

from Document import Document
import numpy
from readDocuments import getDocuments
from readDocuments import getDocumentosFiltrados

from scipy.cluster.vq import kmeans2

#CANTIDAD_CLUSTERS = 500

def createTFIDF(INPUT, filtrado,stopwords_list):
    OUTPUT = INPUT+".arff"


    # RECUPERAMOS DOCUMENTOS
    if(filtrado):
        todo_los_documentos = getDocumentosFiltrados(INPUT, stopwords_list)
    else:
        todo_los_documentos = getDocuments(INPUT,stopwords_list)

    todas_las_palabras = set()

    for document in todo_los_documentos:
        for palabra in document.words:
            todas_las_palabras.add(palabra)
    print("Total de palabras: "+str(len(todas_las_palabras)))


    mapeo_inverso = {}
    lista_palabras = []
    nro_palabra =0
    for palabra in todas_las_palabras:
        lista_palabras.append(palabra)
        mapeo_inverso[palabra] = nro_palabra
        nro_palabra = nro_palabra + 1

    # Vector palabras  lista_palabras = ['hello', 'world', 'jornal', ...]
    # Mapeo inverso    mapeo_inverso  =  {'hello':0, 'world':1, ....... }
    # Documentos     (todo_los_documentos) (set())
    #  | |  |
    #  | |  +----- Titulo
    #  | +-------- Fecha
    #  +---------- Palabras  {'hello': 34, 'journal': 12, ....} palabra hello 34 veces en documento, palabra journal 12 veces, etc.


    tfidf = numpy.zeros(shape=(len(todo_los_documentos), len(lista_palabras)))
    doc = 0
    for document in todo_los_documentos:
        for palabra in document.words:
            tfidf[doc][mapeo_inverso[palabra]] = (document.words[palabra])
        doc = doc + 1


    writer = open(OUTPUT, "w")
    writer.write("@RELATION news\n")
    writer.write("@ATTRIBUTE name STRING\n")

    for palabra in lista_palabras:
        writer.write("@ATTRIBUTE "+palabra.strip('\'"')+" NUMERIC\n")

    writer.write("@DATA\n")
    doc = 0
    for document in todo_los_documentos:
        linea = "\"" + document.title +"\","
        for column in range(0,len(todas_las_palabras)):
            linea = linea + str(tfidf[doc][column])+","
        linea = linea[:-1]
        writer.write(linea+"\n")
        doc = doc + 1
    writer.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                        Aplicacion de Kmeans                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


#resultado = kmeans2(tfidf,CANTIDAD_CLUSTERS)

#print(resultado[1]) # resultado[1] lista de dimension N (donde N es cantidad de documentos) con el nro de cluster al que pertenece cada instancia
