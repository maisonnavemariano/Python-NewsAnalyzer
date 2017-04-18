from readDocuments import getDocuments

INPUT = "../db/noticias/enero"
OUTPUT = "../db/histograma.csv"
documents = getDocuments(INPUT)

word2frec = {}
for document in documents:
    for word in document.words:
        frec_actual = 0 if not word in word2frec else word2frec[word]
        word2frec[word] = frec_actual + document.words[word]

writer = open(OUTPUT, "w")
writer.write("palabra,frecuencia\n")

for palabra in word2frec:
    writer.write(palabra+","+str(word2frec[palabra])+"\n")

writer.close()