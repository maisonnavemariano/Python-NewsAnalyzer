from tfidf import createTFIDF
from generarHistograma import computeIgnoredWords
from Clustering import applyClustering
from LabeledDocument import LabeledDocument

from Document import combinarDocumentos

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


dataset_filtrado = False

documentosEtiquetados_File = Path("../db/pickle/documentosEtiquetados.p")
if not documentosEtiquetados_File.is_file():
    #Crear tf-idf.
    documentos, matriz  = createTFIDF( dataset_filtrado,INPUT ) # luego como stop words usamos l as listas anteriores y las de palabras ignoradas
    #Aplicar clustering Kmeans.
    documentosEtiquetados = applyClustering(matriz,documentos)
    pickle.dump(documentosEtiquetados, open(str(documentosEtiquetados_File), "wb"))
else:
    documentosEtiquetados = pickle.load(open(str(documentosEtiquetados_File), "rb"))


print("Kmeans terminado.")
clusters = getClusters(documentosEtiquetados)
#Guardar resultados.
saveResult(documentosEtiquetados,clusters)

nro = 0
documentosDeCluster = []
for cluster in clusters:
    nuevoDoc = combinarDocumentos(cluster, "clusterNro"+str(nro))
    documentosDeCluster.append(nuevoDoc)
    nro =  1 + nro

#documentos, matriz  = createTFIDF( dataset_filtrado,"../db/noticias/enero",documentosDeCluster )
