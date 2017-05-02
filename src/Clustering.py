from scipy.cluster.vq import kmeans2
from LabeledDocument import LabeledDocument
import re
import datetime
now = datetime.datetime.now()

CONFIG = "../etc/var.config"
def initVar():
    NRO_OF_CLUSTERS = "NRO_OF_CLUSTERS = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(NRO_OF_CLUSTERS):
                k = int(line[len(NRO_OF_CLUSTERS):-1])
    return k
def applyClustering(matrix, lista_documentos):
    k = initVar()
    print("aplicamos Kmeans")
    centroides, etiquetas = kmeans2(matrix,k,minit='points')
    print("Kmeans terminado, almacenamos resultado")
    nro_doc = 0
    documentos_Etiquetados = []
    for etiqueta in etiquetas:
        documentoEtiquetado = LabeledDocument(lista_documentos[nro_doc], etiquetas[nro_doc])
        documentos_Etiquetados.append(documentoEtiquetado)
        nro_doc = nro_doc + 1
    return documentos_Etiquetados,centroides

def getClusters(lista_documentos_etiquetados):
    nro_of_clusters = initVar()
    clusters = []
    for i in range(0,nro_of_clusters):
        clusters.append([])
    for document in lista_documentos_etiquetados:
        cluster_nro = int(document.label)
        clusters[cluster_nro].append(document.document)
    return clusters

def saveResult(documentosEtiquetados,clusters):
    writer = open("../db/resultados/clusters" + re.sub(r'\.[0-9]*', "", str(now)) + ".txt", "w")
    writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    writer.write(" * * * * * * * * * * * * Archivo de Configuración de la ejecución  * * * * * * * * * * *\n")
    writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    with open(CONFIG) as f:
        for line in f:
            writer.write(line)
    writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    for doc in documentosEtiquetados:
        writer.write(str(doc.document.instanceNro) + ': \"' + doc.document.title + '\",cluster' + str(doc.label) + "\n")

    writer.write("\n")
    writer.write(" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *\n")
    writer.write(" * * * * * * * * * * * * Cantidad de instancias por cluster  * * * * * * * * * * * * * *\n")


    nro = 0
    for cluster in clusters:
        writer.write("cluster nro: " + str(nro) + " tamanio: " + str(len(cluster)) + "\n")
        nro = nro + 1
    writer.close()
