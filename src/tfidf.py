#!/usr/bin/python3

from DB_Filter import Document
import numpy

INPUT = "../db/EneroFiltrado"
SMART_STOPWORDS = "../stopwords/myStopList0.1.txt"
OUTPUT = "../db/tfidf_matrix.arff"

# RECUPERAMOS DOCUMENTOS

TITLE = "title: "
DATE  = "date: "
TEXT  = "text: "

todo_los_documentos = set()
todas_las_palabras = set()

with open(INPUT) as f:
    for line in f:
        if line.startswith(TITLE):
            title = line[len(TITLE):len(line)-1]
        if line.startswith(DATE):
            date = line[len(DATE):len(line)-1]
        if line.startswith(TEXT):
            text = line[len(TEXT)+1:len(line)-2]
            document = Document(title)
            document.date = date
            for par in text.split(", "):
                clave = par.split(": ")[0][1:-1] #palabra
                valor = par.split(": ")[1]       # frec
                if "}" in valor:
                    valor = valor[:-1]
                document.words[clave] = int(valor)
                todas_las_palabras.add(clave)
            #print(document.words)
            todo_los_documentos.add(document)


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
#  +---------- Palabras  {'hello':34, 'journal':12, ....} palabra hello 34 veces en documento, palabra journal 12 veces, etc.


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

