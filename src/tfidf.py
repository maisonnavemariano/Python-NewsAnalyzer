#!/usr/bin/python3

from Document import Document
from numpy.linalg import svd
from numpy import diag
import numpy
from readDocuments import getDocuments
from readDocuments import getDocumentosFiltrados

from numpy.linalg import svd
CONFIG = "../etc/var.config"
def initVar():
    SVD_ANALYSIS = "SVD_ANALYSIS = "
    IGNORED_COEFFICIENTS = "IGNORED_COEFFICIENTS = "
    STOPWORD_FILES = "STOPWORDS_FILES = "
    IGNORED_WORDS_FILE = "IGNORED_WORDS_FILE = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(SVD_ANALYSIS):
                svd_analysis = int(line[len(SVD_ANALYSIS):-1])
            if line.startswith(IGNORED_COEFFICIENTS):
                ignored_coeff = int(line[len(IGNORED_COEFFICIENTS):-1])
            if line.startswith(STOPWORD_FILES):
                stopwords = line[len(STOPWORD_FILES)+2:-3].split('\",\"')
            if line.startswith(IGNORED_WORDS_FILE):
                ignored_words_file = line[len(IGNORED_WORDS_FILE)+1:-2]
    return svd_analysis,stopwords, ignored_coeff,ignored_words_file

#SVD_ANLYSIS = True

from scipy.cluster.vq import kmeans2

#CANTIDAD_CLUSTERS = 500

def createTFIDF(INPUT, filtrado): #,stopwords_list, svd_analysis = False, ignored_coefficients = 0 ):
    svd_analysis, stopwords_list,ignored_coefficients, ignored_words_file = initVar()

    stopwords_list.append(ignored_words_file)
    if(svd_analysis):
        OUTPUT = INPUT+"_svd.arff"
    else:
        OUTPUT = INPUT+".arff"

    print("Recuperamos todos los documentos...")
    # RECUPERAMOS DOCUMENTOS
    if(filtrado):
        todo_los_documentos = getDocumentosFiltrados(INPUT)
    else:
        todo_los_documentos = getDocuments(INPUT,stopwords_list)
    print("Recuperamos "+str(len(todo_los_documentos)))
    todas_las_palabras = set()

    print("analizamos cantidad de palabras (dimensiones del dataset)")
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

    print("Construímos matriz TF-IDF")
    tfidf = numpy.zeros(shape=(len(todo_los_documentos), len(lista_palabras)))
    doc = 0
    for document in todo_los_documentos:
        for palabra in document.words:
            tfidf[doc][mapeo_inverso[palabra]] = (document.words[palabra])
        doc = doc + 1
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * ANALISIS DE SEMANTICA LATENTE * * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    if(svd_analysis):
        print("Analisis de semantica latente")
        u, sigma, vt = svd(tfidf, full_matrices=False)

        for i in range (1,ignored_coefficients+1):
            sigma[-i] = 0
        sigma = numpy.diag(sigma)
        tfidf = numpy.dot(numpy.dot(u,sigma), vt)
        print("Analisis de frecuencia latente terminado.")

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * FIN ANALISIS DE SEMANTICA LATENTE * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    print("almacenamos matriz ARFF....")
    writer = open("sigma.txt","w")
    for row in sigma:
        for element in row:
            writer.write(str(element)+" ")
        writer.write("\n")
    print(sigma)
    writer.close()

    writer = open(OUTPUT, "w")
    writer.write("@RELATION news\n")
    writer.write("@ATTRIBUTE DocumentName STRING\n")

    for palabra in lista_palabras:
        writer.write("@ATTRIBUTE "+palabra.strip('\'"')+" NUMERIC\n")
    writer.write('@ATTRIBUTE sectionName {Society,Business,Worldnews,Politics}\n')
    writer.write("@DATA\n")
    doc = 0
    for document in todo_los_documentos:
        linea = "\"" + document.title +"\","
        for column in range(0,len(todas_las_palabras)):
            linea = linea + str(tfidf[doc][column])+","
        linea = linea[:-1]
        writer.write(linea+","+document.sectionName+"\n")
        doc = doc + 1
    writer.close()
    print("matrix construida satisfactoriamente")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                        Aplicacion de Kmeans                                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


#resultado = kmeans2(tfidf,CANTIDAD_CLUSTERS)

#print(resultado[1]) # resultado[1] lista de dimension N (donde N es cantidad de documentos) con el nro de cluster al que pertenece cada instancia
