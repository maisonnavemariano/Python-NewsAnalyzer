from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
from Clustering import applyClustering
from LabeledDocument import LabeledDocument
import datetime
import re
now = datetime.datetime.now()

INPUT = "../db/noticias/enero"
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"

CONFIG = "../etc/var.config"

lines = []
LAST_THRESHOLD = "LAST_THRESHOLD_EXECUTED = "
THRESHOLD = "THRESHOLD = "
with open(CONFIG) as f:
    for line in f:
        if line.startswith(LAST_THRESHOLD):
            last_threshold = int(line[len(LAST_THRESHOLD):-1])
        else:
            lines.append(line)
            if line.startswith(THRESHOLD):
                threshold = int(line[len(THRESHOLD):-1])


writer = open(CONFIG,"w")
for line in lines:
    writer.write(line)
writer.write(LAST_THRESHOLD+str(threshold)+"\n")
writer.close()

# Optional 1 - recalcular palabras ignoradas (frecuencia 1).
if not (last_threshold == threshold):
    print("recomputamos palabras ignoradas...")
    computeIgnoredWords( INPUT,IGNORED_WORDS_FILE) #primero usamos los stop words sin palabras ignoradas (para la generacion)

#Crear tf-idf.
dataset_filtrado = False
documentos, matriz  = createTFIDF(INPUT, dataset_filtrado ) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas

#Aplicar clustering Kmeans.
documentosEtiquetados = applyClustering(matriz,documentos)

#Guardar resultados.
writer = open("../db/resultados/clusters"+re.sub(r'\.[0-9]*',"",str(now))+".txt", "w")
writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
writer.write(" * * * * * * * * * * * * Archivo de Configuración de la ejecución  * * * * * * * * * * *\n")
writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
with open(CONFIG) as f:
    for line in f:
        writer.write(line)
writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
for doc in documentosEtiquetados:
    writer.write(str(doc.document.instanceNro)+': \"'+doc.document.title+'\",cluster'+str(doc.label)+"\n")
writer.close()





