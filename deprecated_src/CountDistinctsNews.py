#!/usr/bin/python3

INPUT = "../db//noticias/enero"
OUTPUT_REPETIDOS = "../db/noticias/titulos_repetidos_enero.txt"
OUTPUT = "../db/Names"

writer = open(OUTPUT_REPETIDOS, "w")
names = set()
names_repetidos = set()
TITLE = "webTitle: "
with open(INPUT) as f:
    for line in f:
        if line.startswith(TITLE):
            title = line[len(TITLE):-1]
            if line[len(TITLE):-1] in names:
                writer.write(line[len(TITLE):-1]+"\n")
            names.add(title)
print("Titulos distintos: "+str(len(names)))

#writer = open(OUTPUT, "w")

#for name in names_repetidos:
#    writer.write(name+"\n")

writer.close()
