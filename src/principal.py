#!/usr/bin/python3

from news_analysis_with_nltk import my_tokenizer
INPUT = '../db/noticias/argentina/argentina2013'

_title_cons = "webTitle: "
_section_cons = "sectionName: "
_date_cons = "webPublicationDate: "
_bodytext_cons = "bodytext: "
_umbral = 2 # se eliminan hasta el umbral inclusive

noticias = []
noticias_tokenized = []
index = 0
todas_las_palabras = set()
lista_todas_las_palabras = []
print("[OK] Abriendo archivo de noticias ... ")
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
            #Construimos estructuras para contabilizar palabras
            todas_las_palabras = todas_las_palabras.union(set(noticias_tokenized[-1][1])) # agregamos palabras del titulo
            todas_las_palabras = todas_las_palabras.union(set(noticias_tokenized[-1][4])) # agregamos palabras del texto
            lista_todas_las_palabras += noticias_tokenized[-1][1] # agregamos a la lista las palabras del titulo
            lista_todas_las_palabras += noticias_tokenized[-1][4] # agregamos a la lista las palabras del texto
            index += 1

indice_palabra = enumerate(todas_las_palabras)

print("[OK] Lista de tokens construida ... ")
# Current State:
# Dos objetos conteniendo todas las noticias:
# noticias -> [(0,'titulo', 'seccion', 'fecha', 'texto'), ... ]
# noticias_tokenized -> [(0,['token_tiluto', ...], 'seccion', 'fecha', ['token_texto', ...]), ... ]

# todas_las_palabras -> {'palabra1', 'palabra2', ...}
# lista_todas_las_palabras -> ['palabra1', 'palabra2', ... , 'palabra1', ...]    #repetidos


print('cantidad de palabras encontradas: ' + str(len(todas_las_palabras)))
map = dict((palabra ,lista_todas_las_palabras.count(palabra)) for palabra in todas_las_palabras)

from collections import defaultdict
_ignored_words = set()
histograma = defaultdict(int)
for palabra in map:
    if map[palabra] <= _umbral:
        _ignored_words.add(palabra)
    histograma[map[palabra]] +=1

print('[OK] Generamos archivo de palabras ignoradas ...')
_ignored_words_file = '../db/noticias/argentina/ignored_words'
with open(_ignored_words_file, 'w') as w:
    for palabra in _ignored_words:
        w.write(palabra+'\n')

print('[OK] Palabras ignoradas generadas ...')
print('[OK] Generando histograma ...')
_histograma_file = '../db/noticias/argentina/histograma.csv'
_writer = open(_histograma_file, 'w')
_writer.write('frecuencia,cantidad\n')
for frec in sorted(histograma):
    _writer.write(str(frec)+','+str(histograma[frec])+'\n')
_writer.close()

print('[OK] histograma generado ...')

