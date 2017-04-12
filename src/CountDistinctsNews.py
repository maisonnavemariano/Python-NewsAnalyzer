#!/usr/bin/python3

INPUT = "../db//noticias/febrero"
#OUTPUT = "../db/Names"

names = set()
TITLE = "webTitle: "
with open(INPUT) as f:
    for line in f:
        if line.startswith(TITLE):
            title = line[len(TITLE):-1]
            names.add(title)
print("Titulos distintos: "+str(len(names)))

#writer = open(OUTPUT, "w")

#for name in names:
#    writer.write(name+"\n")

#writer.close()
