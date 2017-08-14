#!/usr/bin/python3
# Script que permite leer archivos de noticias generados por generarBase.py.
# Genera objetos tipo Documento, con aquellos articulos validos.
# Retornando una lista con documentos ya prefiltrados.

from Article import Article
from Document import Document


import time

date_time = '29.08.2011 11:05:02'
pattern = '%Y-%m-%dT%H:%M:%SZ'



CONFIG = "../etc/var.config"
FRECUENCIA_TITULOS = "FRECUENCIA_TITULOS = "
def initVar():
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(FRECUENCIA_TITULOS):
                frec_titulos = int(line[len(FRECUENCIA_TITULOS):-1])
    return frec_titulos

def getDocuments(INPUT,stopwords_files):
    frec_titulos = initVar()
    #stopwords_files = ["../stopwords/SmartStoplist.txt", "../stopwords/ignored_words.txt"]
    stopwords = []
    for sw_file in stopwords_files:
        with open(sw_file) as f:
            words = f.read().splitlines()
        stopwords = stopwords + words
    stopwords = set(stopwords)

    TITLE       = "webTitle: "
    SECTION     = "sectionName: "
    HEADLINE    = "headline: "
    TRAILTEXT   = "trailText: "
    DATE        = "webPublicationDate: "
    BODY        = "bodytext: "
    INSTANCE_NRO = "instanceNro: "
    articles = set()
    documents = []
    total_articles = 0

    with open(INPUT) as f:
        for line in f:
            if line.startswith(INSTANCE_NRO):
                instance_nro = int(line[len(INSTANCE_NRO):-1])
            if(line.startswith(TITLE)):
                title = line[len(TITLE):-1];
                article = Article(title);
                article.instanceNro = instance_nro
            if(line.startswith(SECTION)):
                section = line[len(SECTION):-1];
                article.sectionName = section;
            if(line.startswith(HEADLINE)):
                headline = line[len(HEADLINE):-1];
                article.headline = headline
            if(line.startswith(TRAILTEXT)):
                trailtext = line[len(TRAILTEXT):-1];
                article.trailText = trailtext
            if(line.startswith(DATE)):
                date = line[len(DATE):-1];
                article.date = date
            if(line.startswith(BODY)):
                body = line[len(BODY):-1];
                article.bodyText =  body
                total_articles = total_articles + 1
                if (article.isValidArticle()):
                    articles.add(article)

    for article in articles:
        document = Document(article.title,article.sectionName)
        # ponderamos el titulo
        for i in range(0,frec_titulos):
            document.addText(article.title, stopwords)
        document.instanceNro = article.instanceNro
        document.addText(article.bodyText,stopwords)
        document.addText(article.trailText,stopwords)
        document.addText(article.headline,stopwords)
        document.addText(article.sectionName,stopwords)
        epoch = int(time.mktime(time.strptime(article.date, pattern)))
        document.date = epoch
        document.setOriginalText(article.bodyText)
        documents.append(document)

    return documents
