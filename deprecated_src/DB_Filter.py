#!/usr/bin/python3
from Article import Article
from Document import Document

stopwords = []
with open("../stopwords/SmartStoplist.txt") as f:
    stopwords = f.read().splitlines()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)



INPUT = "../db/noticias/enero"
OUTPUT = "../db/EneroFiltrado"

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
    document.addText(article.bodyText, stopwords)
    document.addText(article.trailText, stopwords)
    document.addText(article.headline, stopwords)
    document.addText(article.sectionName, stopwords)
    document.date = article.date
    documents.add(document)


todas_las_palabras = set()
for d in documents:
    for word in d.words:
        todas_las_palabras.add(word)


writer = open(OUTPUT,"w")
for document in documents:
    writer.write("title: "+document.title+"\n")
    writer.write("date: "+document.date+"\n")
    writer.write("section: "+document.sectionName)
    writer.write("text: "+str(document.words)+"\n")



print("Hay "+str(len(articles))+" articulos validos de "+str(total_articles)+".")
print("Hay un total de "+str(len(todas_las_palabras))+ " palabras distintas en el dataset.")