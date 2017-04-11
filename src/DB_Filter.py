#!/usr/bin/python3
from Article import Article

stopwords = []
with open("../stopwords/SmartStoplist.txt") as f:
    stopwords = f.read().splitlines()

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

# * * * * * * * * * * * * * * * * * * Document class Definition * * * * * * * * * * * * * * * * * *
class Document(object):

    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def __init__(self, title, date = ""):
        self.words = {}
        self.date = date
        self.title = title

    def addText(self, text):
        text = text.lower()
        text = "".join(c for c in text if c in self.PERMITTED_CHARS)
        words_array = text.split(" ")
        for word in words_array:
            if not word in stopwords and len(word)>0 and not hasNumbers(word):
                if word in self.words:
                    self.words[word] = self.words[word]+1
                else:
                    self.words[word] = 1

# * * * * * * * * * * * * * * * * * *  End of class Definition  * * * * * * * * * * * * * * * * * *

INPUT = "../db/Enero"
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

for article in articles:
    document = Document(article.title)
    document.addText(article.bodyText)
    document.addText(article.trailText)
    document.addText(article.headline)
    document.addText(article.sectionName)
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
    writer.write("text: "+str(document.words)+"\n")


print("Hay "+str(len(articles))+" articulos validos de "+str(total_articles)+".")
print("Hay un total de "+str(len(todas_las_palabras))+ " palabras distintas en el dataset.")