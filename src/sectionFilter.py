#!/usr/bin/python3

INPUT = "../db/Enero"
OUTPUT = "../db/Sections"

SECTION = "sectionName: "
sections = set()

with open(INPUT) as f:
    for line in f:
        if(line.startswith(SECTION)):
            section = line[len(SECTION):-1]
            sections.add(section)

writer = open(OUTPUT, "w")
for section in sections:
    writer.write(section+"\n")
writer.close()

