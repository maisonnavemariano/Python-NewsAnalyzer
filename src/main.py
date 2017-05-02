from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
from Clustering import applyClustering
from LabeledDocument import LabeledDocument

from Document import combinarDocumentos

import numpy as np
from Clustering import getClusters
from Clustering import saveResult
from pathlib import Path
import pickle

resultado_Clustering = None

INPUT = "../db/noticias/enero"
IGNORED_WORDS_FILE = "../stopwords/ignored_words.txt"
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * * *  CONFIGURACION  * * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
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


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
# * * * * * * * * * * * *  Fin CONFIGURACION  * * * * * * * * * * * *
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


documentosEtiquetados_File = Path("../db/pickle/documentosEtiquetados.p")
centroides_File = Path("../db/pickle/centroides.p")
if not documentosEtiquetados_File.is_file() or not  centroides_File.is_file():
    #Crear tf-idf.
    documentos, matriz  = createTFIDF( INPUT) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas
    #Aplicar clustering Kmeans.
    documentosEtiquetados,centroides = applyClustering(matriz,documentos)
    pickle.dump(documentosEtiquetados, open(str(documentosEtiquetados_File), "wb"))
    pickle.dump(centroides, open(str(centroides_File),"wb"))

else:
    documentosEtiquetados = pickle.load(open(str(documentosEtiquetados_File), "rb"))
    centroides = pickle.load(open(str(centroides_File), "rb"))


print("Kmeans terminado.")
clusters = getClusters(documentosEtiquetados)
#Guardar resultados.
saveResult(documentosEtiquetados,clusters)

columnas = ["cantidad_noticias","fecha_centroide","error_cuadratico","varianza_fechas"]
dataset_clusters = np.zeros(shape = (len(clusters),len(columnas)))

# Columna cantidad_noticias
c = 0
for cluster in clusters:
    dataset_clusters[c][0] = len(cluster)
    dataset_clusters[c][1] = centroides[c][len(centroides[c])-1]
    c = c +1

writer = open("../db/clusters.tmp", "w")
for row in dataset_clusters:
    line = ""
    for element in row:
        line = line +" "+str(element)
    writer.write(line+"\n")
writer.close()



#documentos, matriz  = createTFIDF( dataset_filtrado,"../db/noticias/enero",documentosDeCluster )
