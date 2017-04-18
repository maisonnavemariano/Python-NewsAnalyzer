from readDocuments import getDocuments
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   GENERA HISTOGRAMA Y ARCHIVO DE PALABRAS IGNORADAS                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

INPUT = "../db/noticias/enero"
OUTPUT = "../db/histograma.csv"
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"
threshold = 3 # solo palabras con 3 o menos apariciones.
documents = getDocuments(INPUT)

word2frec = {}
for document in documents:
    for word in document.words:
        frec_actual = 0 if not word in word2frec else word2frec[word]
        word2frec[word] = frec_actual + document.words[word]


writer = open(OUTPUT, "w")
writer_ignored = open(IGNORED_WORDS_FILE, "w")
writer.write("palabra,frecuencia\n")
writer.write("palabra,frecuencia\n")

for palabra in word2frec:
    writer.write(palabra+","+str(word2frec[palabra])+"\n")
    if(word2frec[palabra] <= threshold):
        writer_ignored.write(palabra+"\n")

writer_ignored.close()
writer.close()