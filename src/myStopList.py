
from DB_Filter import Document
import operator
INPUT = "../db/EneroFiltrado"
threshold1 = 0.10
threshold2 = 0.25
threshold3 = 0.50
threshold4 = 0.80
OUTPUT1 = "../stopwords/myStopList"+str(threshold1)+".txt"
OUTPUT2 = "../stopwords/myStopList"+str(threshold2)+".txt"
OUTPUT3 = "../stopwords/myStopList"+str(threshold3)+".txt"
OUTPUT4 = "../stopwords/myStopList"+str(threshold4)+".txt"


writer1 = open(OUTPUT1, "w")
writer2 = open(OUTPUT2, "w")
writer3 = open(OUTPUT3, "w")
writer4 = open(OUTPUT4, "w")

TITLE = "title: "
DATE  = "date: "
TEXT  = "text: "

todo_los_documentos = set()
todas_las_palabras = set()
with open(INPUT) as f:
    for line in f:
        if line.startswith(TITLE):
            title = line[len(TITLE):len(line)-1]
        if line.startswith(DATE):
            date = line[len(DATE):len(line)-1]
        if line.startswith(TEXT):
            text = line[len(TEXT):len(line)-1]
            document = Document(title)
            document.date = date
            for par in text.split(", "):
                clave = par.split(": ")[0][1:-1]
                valor = par.split(": ")[1]
                document.words[clave] = valor
                todas_las_palabras.add(clave)
            todo_los_documentos.add(document)

# Por cada palabra, tenemos que ver en cuantos documentos aparece. Si aparece en 9.997, quiere decir que aparee en todos los documentos
# eso la convierte en una palabra poco representativa.

palabra_2_frec = {}

for palabra in todas_las_palabras:
    palabra_2_frec[palabra] = 0
    for document in todo_los_documentos:
        if palabra in document.words:
            palabra_2_frec[palabra] = palabra_2_frec[palabra]  + 1
print(sorted(palabra_2_frec.items(), key=operator.itemgetter(1)))

# 100%           _________________  9.997 (len(todo_los_documentos))
#  10% (umbral)  _________________ x = cantidad de documentos para alcanzar el umbral
# si cantidad de apariciones de una palabra >= x entonces debe ser ignorada.           INCORPORAR AL STOPWORD LIST
# si cantidad de apariciones de una palabra < x  entonces debe aparecer
#
umbral1 = (threshold1*len(todo_los_documentos))  # umbral = x
umbral2 = (threshold2*len(todo_los_documentos))  # umbral = x
umbral3 = (threshold3*len(todo_los_documentos))  # umbral = x
umbral4 = (threshold4*len(todo_los_documentos))  # umbral = x

for palabra in palabra_2_frec:
    if palabra_2_frec[palabra] > umbral1:
        writer1.write(palabra[1:-1]+"\n")
    if palabra_2_frec[palabra] > umbral2:
        writer2.write(palabra[1:-1]+"\n")
    if palabra_2_frec[palabra] > umbral3:
        writer3.write(palabra[1:-1]+"\n")
    if palabra_2_frec[palabra] > umbral4:
        writer4.write(palabra[1:-1]+"\n")

writer1.close()
writer2.close()
writer3.close()
writer4.close()
print("Se levantaron "+str(len(todo_los_documentos))+" documentos.")