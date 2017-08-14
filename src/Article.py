#!/usr/bin/python3
# Clase para representar un archivo (noticia) de The Guardian.
# Permite determinar cuando un archivo es invalido. Esto es cuando el cuerpo del texto es vacío, o pertenece a secciones consideradas irrelevantes (como por ejemplo:
# Music, Film, Sport, etc).

import re

CONFIG = "../etc/var.config"
def initVar():
    ALLOWED_SECTIONS = "ALLOWED_SECTIONS = "
    with open(CONFIG) as f:
        for line in f:
            if line.startswith(ALLOWED_SECTIONS):
                allowed_sections = line[len(ALLOWED_SECTIONS)+2:-3].split('","')
    return allowed_sections


class Article(object):
    ALLOWED_SECTIONS = initVar()
    def __init__(self, title, sectionName='', headline='', trailtext='', bodyText='', date='',instanceNro = -1): #Default values '' if one of the parameters is not given.
        self.instanceNro = instanceNro
        self.title       = title;
        self.sectionName = sectionName;
        self.headline    = headline;
        self.trailText   = trailtext;
        self.bodyText    = bodyText;
        self.date        = date;


    def isValidArticle(self):
        return len(self.bodyText)>0 and self.sectionName in self.ALLOWED_SECTIONS;

    def print(self):
        print(self.title + self.date );
