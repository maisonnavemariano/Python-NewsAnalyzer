#!/usr/bin/python3

from news_analysis_with_nltk import my_tokenizer
INPUT = '../db/noticias/argentina/argentina2013'

_title_cons = "webTitle: "
_section_cons = "sectionName: "
_date_cons = "webPublicationDate: "
_bodytext_cons = "bodytext: "

noticias = []
noticias_tokenized = []
index = 0
with open(INPUT) as f:
    for line in f:
        if line.startswith(_title_cons):
            title = line[len(_title_cons):-1]
        if line.startswith(_section_cons):
            section = line[len(_section_cons):-1]
        if line.startswith(_date_cons):
            date = line[len(_date_cons):-1]
        if line.startswith(_bodytext_cons):
            body = line[len(_bodytext_cons):-1]
            noticias.append((index,title,section,date,body))
            noticias_tokenized.append( (index,my_tokenizer(title),section,date,my_tokenizer(body))  )
            index += 1

todas_las_palabras = set()
lista_todas_las_palabras = []
for noticia in noticias_tokenized:
    print("title: "+str(noticia[1]))
    for palabra in noticia[1]:
        todas_las_palabras.add(palabra)
        lista_todas_las_palabras.append(palabra)
    print("body: "+str(noticia[4]))
    for palabra in noticia[4]:
        todas_las_palabras.add(palabra)
        lista_todas_las_palabras.append(palabra)

print('cantidad de palabras ' + str(len(todas_las_palabras)))
map = dict((palabra ,lista_todas_las_palabras.count(palabra)) for palabra in todas_las_palabras)

count_frec_1 = 0
count_frec_2 = 0
count_frec_3 = 0

for palabra in map:
    if map[palabra] ==1:
        count_frec_1 += 1
    if map[palabra] ==2:
        count_frec_2 += 1
    if map[palabra] ==3:
        count_frec_3 += 1

print("una unica aparicion: " + str(count_frec_1))
print("dos apariciones: "+str(count_frec_2))
print("tres apariciones: "+str(count_frec_3))


