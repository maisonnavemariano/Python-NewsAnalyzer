from scipy.cluster.vq import kmeans2
from LabeledDocument import LabeledDocument
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
    centroides, etiquetas = kmeans2(matrix,k)
    print("Kmeans terminado, almacenamos resultado")
    nro_doc = 0
    for etiqueta in etiquetas:
        documentoEtiquetado = LabeledDocument(lista_documentos[nro_doc], etiqueta[nro_doc])
        nro_doc = nro_doc + 1