#!/usr/bin/python3
from Article import Article
from Document import Document
def getDocuments(INPUT,stopwords_files):
    #stopwords_files = ["../stopwords/SmartStoplist.txt", "../stopwords/ignored_words.txt"]
    stopwords = []
    for sw_file in stopwords_files:
        with open(sw_file) as f:
            words = f.read().splitlines()
        stopwords = stopwords + words


    TITLE       = "webTitle: "
    SECTION     = "sectionName: "
    HEADLINE    = "headline: "
    TRAILTEXT   = "trailText: "
    DATE        = "webPublicationDate: "
    BODY        = "bodytext: "

    articles = set()
    documents = set()
    total_articles = 0

    with open(INPUT) as f:
        for line in f:
            if(line.startswith(TITLE)):
                title = line[len(TITLE):-1];
                article = Article(title);
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
        document.addText(article.title, stopwords)


        document.addText(article.bodyText,stopwords)
        document.addText(article.trailText,stopwords)
        document.addText(article.headline,stopwords)
        document.addText(article.sectionName,stopwords)
        document.date = article.date
        documents.add(document)
    return documents

def getDocumentosFiltrados(INPUT):
    TITLE = "title: "
    DATE = "date: "
    TEXT = "text: "
    SECTION = "section: "

    documents = set()
    with open(INPUT) as f:
        for line in f:
            if line.startswith(TITLE):
                title = line[len(TITLE):-1]
                document_aux = Document(title)
            if line.startswith(DATE):
                date = line[len(DATE):-1]
                document_aux.date = date
            if line.startswith(SECTION):
                section = line[len(SECTION):-1]
                document_aux.sectionName = section
            if line.startswith(TEXT):
                #{'hola': 2, 'world': 1, 'bla': 1}
                text = line[len(TEXT):-1]
                #sacamos llaves
                text = text[1:-1]
                for par in text.split(", "):
                    palabra = par.split(": ")[0]
                    palabra = palabra[1:-1] # le sacamos las comillas.
                    frecuencia = par.split(": ")[1]
                    document_aux.words[palabra] = frecuencia
                documents.add(document_aux)
    return documents