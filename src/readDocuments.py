#!/usr/bin/python3
from Article import Article
from Document import Document
def getDocuments(INPUT):
    stopwords_files = ["../stopwords/SmartStoplist.txt", "../stopwords/ignored_words.txt"]
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
        document = Document(article.title)
        document.addText(article.bodyText,stopwords)
        document.addText(article.trailText,stopwords)
        document.addText(article.headline,stopwords)
        document.addText(article.sectionName,stopwords)
        document.date = article.date
        documents.add(document)
    return documents