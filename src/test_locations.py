#!/usr/bin/python3
import pickle
import countryAnalysis
import re
import datetime
import tfidf
import Clustering
now = datetime.datetime.now()

CONFIG = "../etc/var.config"

def initVar():
    selected_country_const = "SELECTED_COUNTRY = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(selected_country_const):
                selected_country = line[len(selected_country_const):-1]
    return selected_country


OUTPUT = "../db/resultados/rel_pais_{0}_date_{1}.txt"
fecha = re.sub(r'\.[0-9]*', "", str(now))
pais = initVar()

OUTPUT = OUTPUT.format(pais,fecha)


INPUT = "../db/pickle/map_location2code.p"
COUNTRIES = "../db/pickle/map_country2code.p"
location2code = pickle.load( open(INPUT, "rb"))
country2code = pickle.load(open(COUNTRIES, "rb"))

print("cantidad de paises en la lista: "+str(len(country2code)))

lista = countryAnalysis.sortByRelevance()

print("Documentos ordenados por relevancia..")

index = 0
writer =  open(OUTPUT, "w")
for elem in lista:
    writer.write(str(index) +": "+elem[0].title+", "+str(elem[1])+"\n")
    index = index +1



listaDocumentosDelPais = [x for (x,_) in lista]

# Aplicar clustering sobre lista ordenada, mostrar resultados...

todo_los_documentos, tfidf, _ = tfidf.createTFIDF( list_documents= listaDocumentosDelPais)
print("comienza clustering de documentos en clusters")
documentos_Etiquetados,_ = Clustering.applyClustering(tfidf, listaDocumentosDelPais)

clusters = Clustering.getClusters(documentos_Etiquetados)
cluster_nro = 0
for cluster in clusters:
    writer.write(" * * * * * * * * * * * * * cluster nro. {0} * * * * * * * * * *".format(str(cluster_nro))+"\n")
    for doc in cluster:
        writer.write(doc.title+"\n")
    cluster_nro = cluster_nro +1

writer.close()
Clustering.saveResult(documentos_Etiquetados,clusters)