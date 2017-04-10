#!/usr/bin/python3
from Article import Article

INPUT = "../db/Enero"
OUTPUT = "../db/EneroFiltrado"

TITLE       = "webTitle: "
SECTION     = "sectionName: "
HEADLINE    = "headline: "
TRAILTEXT   = "trailText: "
DATE        = "webPublicationDate: "
BODY        = "bodytext: "

articles = set()
total_articles = 0

with open(INPUT) as f:
    for line in f:
        if(line.startswith(TITLE)):
            title = line[len(TITLE):len(line)-1];
            article = Article(title[0:len(title)-1]);
        if(line.startswith(SECTION)):
            section = line[len(SECTION):len(line)-1];
            article.sectionName = section;
        if(line.startswith(HEADLINE)):
            headline = line[len(HEADLINE):len(line)-1];
            article.headline = headline
        if(line.startswith(TRAILTEXT)):
            trailtext = line[len(TRAILTEXT):len(line)-1];
            article.trailText = trailtext
        if(line.startswith(DATE)):
            date = line[len(DATE):len(line)-1];
            article.date = date
        if(line.startswith(BODY)):
            body = line[len(BODY):len(line)-1];
            article.bodyText =  body
            total_articles = total_articles + 1
            if (article.isValidArticle()):
                articles.add(article)

print("Hay "+str(len(articles))+" articulos validos de "+str(total_articles)+".")
