#!/usr/bin/python3
import re,datetime,pickle,readDocuments
from dictionaryAnalyze import DiccionarioPalabras
from pathlib import Path

INPUT = "../db/noticias/noticias2013"

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

OUTPUT_DOCS = Path("../db/pickle/todos_los_documentos.p")
def economic_print():
    stopwords_files, ignored_words_file,selected_country = initVar()
    stopwords_files.append(ignored_words_file)
    if not OUTPUT_DOCS.is_file():
        documentos = readDocuments.getDocuments(INPUT, stopwords_files)
        pickle.dump(documentos, open(str(OUTPUT_DOCS),"wb") )
    else:
        documentos = pickle.load(open(str(OUTPUT_DOCS),"rb"))


    listaDocumentosDelPais = [documento for documento in documentos if selected_country in documento.locations]
    print("cantidad de documentos del pais: {0}".format(str(len(listaDocumentosDelPais))))
    dic = DiccionarioPalabras()

    sortedList = dic.sortByEconomicRelevance(listaDocumentosDelPais)
    indice = 0
    for element in sortedList:
        print("{0}: {1}".format(indice,element.title))
        indice +=1

economic_print()

