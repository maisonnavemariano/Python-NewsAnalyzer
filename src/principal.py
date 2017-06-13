#!/usr/bin/python3

from news_analysis_with_nltk import my_tokenizer
INPUT = '../db/noticias/noticias2013'

TITLE = "webTitle: "
SECTION = "sectionName: "
HEADLINE = "headline: "
TRAILTEXT = "trailText: "
DATE = "webPublicationDate: "
BODY = "bodytext: "
INSTANCE_NRO = "instanceNro: "

MAPEO_PAISES = "../db/pickle/map_country2code.p"
import pickle
_country2code = pickle.load(open(MAPEO_PAISES, "rb"))

country =  "argentina"

noticias = []
indice = 0
todas_las_palabras = set()
# with open(INPUT) as f:
#     for line in f:
#         valor = line[:-1]
#         if line.startswith(TITLE):
#             title = line[len(TITLE):]
#         if line.startswith(SECTION):
#             section = line[len(SECTION):]
#         if line.startswith(DATE):
#             date = line[len(DATE):]
#         if line.startswith(BODY):
#             text = line[len(BODY):]
#             if "argentina" in text.lower() or "argentina" in title.lower():
#                 tokens = my_tokenizer(text)
#                 noticias.append((indice, title, section, date,  ))
#                 todas_las_palabras =todas_las_palabras.union(set(tokens))
#                 print(str(indice))
#                 indice +=  1
#
# noticias_file = '../db/noticias/noticias_tokenized.p'
# pickle.dump(noticias,open(noticias_file, "wb"))


noticias_file = '../db/noticias/noticias_tokenized.p'
noticias = pickle.load(open(noticias_file, "rb"))
print("cantidad de noticias: "+str(len(noticias)))
lista_palabras = []
for noticia in noticias:
    todas_las_palabras = todas_las_palabras.union(set(noticia[4]))
    lista_palabras = lista_palabras + noticia[4]

print("todas las palabras: "+str(len(todas_las_palabras)))
print("palabras que aparecen más de una vez: "+str(len([elem for elem in todas_las_palabras if lista_palabras.count(elem)>3])))







