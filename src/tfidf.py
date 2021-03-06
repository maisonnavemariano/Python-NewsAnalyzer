#!/usr/bin/python3
# Script para la aplicacion de tfidf.

from Document import Document
from numpy.linalg import svd
from numpy import diag
import numpy
from readDocuments import getDocuments
from scipy.cluster.vq import kmeans2
from numpy.linalg import svd
import math

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
            if line.startswith(SVD_ANALYSIS):
                svd_analysis = (line[len(SVD_ANALYSIS):-1]) == "True"
            if line.startswith(IGNORED_COEFFICIENTS):
                ignored_coeff = int(line[len(IGNORED_COEFFICIENTS):-1])
            if line.startswith(STOPWORD_FILES):
                stopwords = line[len(STOPWORD_FILES)+2:-3].split('\",\"')
            if line.startswith(IGNORED_WORDS_FILE):
                ignored_words_file = line[len(IGNORED_WORDS_FILE)+1:-2]
            if line.startswith(SAVE_ARFF):
                save_arff = line[len(SAVE_ARFF):-1] == "True"
            if line.startswith(CON_FECHA):
                con_fecha = line[len(CON_FECHA):-1] == "True"
    return svd_analysis,stopwords, ignored_coeff,ignored_words_file,save_arff,con_fecha


def _normalizeRow(nroRow, matrix):
    module = math.sqrt(sum(math.pow(x,2) for x in matrix[nroRow] ))
    matrix[nroRow] = [elem/module for elem in matrix[nroRow]]


def createTFIDF( INPUT="", list_documents=None): #,stopwords_list, svd_analysis = False, ignored_coefficients = 0 ):
    svd_analysis, stopwords_list,ignored_coefficients, ignored_words_file,save_arff,fecha = initVar()

    stopwords_list.append(ignored_words_file)

    if INPUT == "":
        OUTPUT = "../db/resultados/matrix.arff"
    else:
        if(svd_analysis):
            OUTPUT = INPUT+"_svd.arff"
        else:
            OUTPUT = INPUT+".arff"

    if(list_documents == None):
        print("Recuperamos todos los documentos...")
        # RECUPERAMOS DOCUMENTOS
        todo_los_documentos = getDocuments(INPUT,stopwords_list)
        print("Recuperamos "+str(len(todo_los_documentos)))
    else:
        todo_los_documentos = list_documents


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
    idf = [0]*len(todas_las_palabras)
    for palabra in todas_las_palabras:
        cant_apariciones = 0
        for document in todo_los_documentos:
            if palabra in document.words:
                cant_apariciones = + 1
        idf[mapeo_inverso[palabra]] = math.log(float(len(todo_los_documentos)) / float(cant_apariciones) , 10)


    tfidf = numpy.zeros(shape=(len(todo_los_documentos), len(lista_palabras))) # Más uno por la fila con las fechas (epoch)
    doc = 0

    for document in todo_los_documentos:
        for palabra in document.words:
            indice_palabra = mapeo_inverso[palabra]
            tfidf[doc][indice_palabra] = float((document.words[palabra])) *  idf[indice_palabra]
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
    # * * * * * * * * * * * * * * * * * * * * AGREGADO DE EPOCH COMO ATRIBUTO * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    if(fecha):
        tfidf_conFecha = numpy.zeros(shape=(len(todo_los_documentos), len(lista_palabras)+1))
        # copiamos primeros elementos de tfidf.
        for row in range(0,len(todo_los_documentos)):
            for column in range (0,len(todas_las_palabras)):
                tfidf_conFecha[row][column] = tfidf[row][column]
        # agregamos fechas
        for doc in range(0,len(todo_los_documentos)):
            tfidf_conFecha[doc][len(todas_las_palabras)] = todo_los_documentos[doc].date

        tfidf = tfidf_conFecha

    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * GUARDAMOS MATRIZ EN ARCHIO ARFF * * * * * * * * * * * * * * * * * * * * *
    # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    if (save_arff):
        print("almacenamos matriz ARFF....")
        writer = open(OUTPUT, "w")
        writer.write("@RELATION news\n")
        writer.write("@ATTRIBUTE DocumentName STRING\n")

        for palabra in lista_palabras:
            writer.write("@ATTRIBUTE "+palabra.strip('\'"')+" NUMERIC\n")
        if(fecha):
            writer.write("@ATTRIBUTE FechaDeLaNoticia NUMERIC\n")

        writer.write('@ATTRIBUTE sectionName {Society,Business,Worldnews,Politics}\n')
        writer.write("@DATA\n")
        doc = 0
        for document in todo_los_documentos:
            linea = "\"" + document.title +"\","
            for column in range(0,len(tfidf[0])):
                linea = linea + str(tfidf[doc][column])+","
            linea = linea[:-1]
            writer.write(linea+","+document.sectionName+"\n")
            doc = doc + 1
        writer.close()
        print("matrix construida satisfactoriamente")
    return todo_los_documentos, tfidf, lista_palabras

def createSimilarityMatrix(matrix):
    rowcount, _ = matrix.shape
    matrixCopy = numpy.copy(matrix)
    for row in range(rowcount):
        _normalizeRow(row,matrixCopy)
    transpose = numpy.transpose(matrixCopy)
    similarityMatrix = numpy.dot(matrixCopy,transpose)
    return similarityMatrix