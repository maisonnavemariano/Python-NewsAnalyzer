from readDocuments import getDocuments
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                   GENERA HISTOGRAMA Y ARCHIVO DE PALABRAS IGNORADAS                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
CONFIG = "../etc/var.config"

def initVar():
    THRESHOLD = "THRESHOLD = "
    STOPWORD_FILES = "STOPWORDS_FILES = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(THRESHOLD):
                threshold = int(line[len(THRESHOLD):-1])
            if line.startswith(STOPWORD_FILES):
                stopwords = line[len(STOPWORD_FILES)+2:-3].split('\",\"')
    return threshold,stopwords



def computeIgnoredWords(INPUT,IGNORED_WORDS_FILE):
    threshold, stopwords_list = initVar()
    OUTPUT = "../db/histograma.csv"
    #threshold = 1 # solo palabras con 3 o menos apariciones.
    print("Leemos documentos. . .")
    documents = getDocuments(INPUT,stopwords_list)
    print("Documentos Leídos: "+str(len(documents))+".")

    word2frec = {}
    for document in documents:
        for word in document.words:
            frec_actual = 0 if not word in word2frec else word2frec[word]
            word2frec[word] = frec_actual + document.words[word]
    print("Frecuencias computadas...eliminamos frecuencias menores a "+str(threshold)+".")

    writer = open(OUTPUT, "w")
    writer_ignored = open(IGNORED_WORDS_FILE, "w")
    writer.write("palabra,frecuencia\n")
    writer_ignored.write("palabra,frecuencia\n")
    no_ignoradas = 0
    for palabra in word2frec:
        writer.write(palabra+","+str(word2frec[palabra])+"\n")
        if(word2frec[palabra] <= threshold):
            writer_ignored.write(palabra+"\n")
            no_ignoradas = no_ignoradas + 1


    writer_ignored.close()
    print("total de palabras: "+str(len(word2frec)))
    print("total de palabras ignoradas: "+(str(len(word2frec)-no_ignoradas) ))
    print("palabras aceptadas: "+str(no_ignoradas))
    writer.close()
    print("Archivo de Palabras generado exitosamente.")