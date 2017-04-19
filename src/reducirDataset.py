#!/usr/bin/python3

from readDocuments import getDocuments
import random

INPUT  = "../db/noticias/enero"
OUTPUT = "../db/noticias/enero100"

# Recuperamos y filtramos documentos
documents = getDocuments(INPUT)
documents100 = random.sample(list(documents), 100)

print("cantidad de documentos restantes: "+str(len(documents100)))



writer = open(OUTPUT, "w")
TITLE = "title: "
DATE = "date: "
TEXT = "text: "

for document in documents100:
    writer.write("title: "+document.title+"\n")
    writer.write("date: "+document.date+"\n")
    writer.write("text: "+str(document.words)+"\n")

writer.close()