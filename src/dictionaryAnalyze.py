#!/usr/bin/python3

import re
import numpy

INPUT = "../db/H4Lvd_Dictionary/inqdict.txt"

PATTERN_DEFINITION = '\ *\|\ *.*'
PATTERN_MULTIPLE_DEFINITIONS = "^[A-Z]*#[0-9]*\ "

#http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
#http://www.wjh.harvard.edu/~inquirer/homecat.htm

#Entryword Source Pos Neg Pstv Affil Ngtv Hostile Strng Power Weak Subm Actv Psv Pleasure Pain Arousal EMOT Feel Virtue Vice Ovrst Undrst Acad Doctr Econ* Exch ECON Exprs Legal
# Milit Polit* POLIT Relig Role COLL Work Ritual Intrel Race Kin* MALE Female Nonadlt HU ANI PLACE Social Region Route Aquatic Land Sky Object Tool Food Vehicle Bldgpt Natobj
# Bodypt Comnobj Comform COM Say Need Goal Try Means Ach Persist Complt Fail Natpro Begin Vary Change Incr Decr Finish Stay Rise Move Exert Fetch Travel Fall Think Know Causal
# Ought Percv Comp Eval EVAL Solve Abs* ABS Qual Quan NUMB ORD CARD FREQ DIST Time* TIME Space POS DIM Dimn Rel COLOR Self Our You Name Yes No Negate Intrj IAV DAV SV IPadj IndAdj
# POWGAIN POWLOSS POWENDS POWAREN POWCON POWCOOP POWAPT POWPT POWDOCT POWAUTH POWOTH POWTOT RCTETH RCTREL RCTGAIN RCTLOSS RCTENDS RCTTOT RSPGAIN RSPLOSS RSPOTH RSPTOT AFFGAIN
# AFFLOSS AFFPT AFFOTH AFFTOT WLTPT WLTTRAN WLTOTH WLTTOT WLBGAIN WLBLOSS WLBPHYS WLBPSYC WLBPT WLBTOT ENLGAIN ENLLOSS ENLENDS ENLPT ENLOTH ENLTOT SKLAS SKLPT SKLOTH SKLTOT
# TRNGAIN TRNLOSS TRANS MEANS ENDS ARENAS PARTIC NATIONS AUD ANOMIE NEGAFF POSAFF SURE IF NOT TIMESP FOOD FORM Othertags Definition



class DiccionarioPalabras(object):

    diccionario = {}
    #_RELATED_TO_ECONOMICS = ["econ*"]#,"ECON"]
    _ECON_CAT_1 = 'Econ*'
    _ECON_CAT_2 = "ECON"
    _econ_set_1 = set()
    _econ_set_2 = set()
    _econ_set_3 = set()
    _econ_set_4 = set()
    _diccionarioEconomico = set()
    def __init__(self):
        print("Generamos diccionario de palabras H4Lvd")
        # Leemos archivo para generar categorias
        with open(INPUT) as f:
            primeraLinea = f.readline()[:-1] # Descartamos primera linea
            todas_las_palabras = []
            todas_las_categorias = set()
            diccionario = {} # Palabra --> set()
            for line in f:
                if not re.search(PATTERN_MULTIPLE_DEFINITIONS,line):
                    line = re.sub(PATTERN_DEFINITION, "", line[:-1])
                    parts = line.split(" ")
                    palabra = parts[0].lower()
                    categorias = set(parts[2:])
                    diccionario[palabra] = categorias
                    todas_las_categorias = todas_las_categorias.union(categorias)
        print("[OK]Diccionario finalizado.")
        for palabra in diccionario:
            if self._ECON_CAT_1 in diccionario[palabra]:
                self._econ_set_1.add(palabra)
            if self._ECON_CAT_2 in diccionario[palabra]:
                self._econ_set_2.add(palabra)
        self._econ_set_3 = self._econ_set_1.union(self._econ_set_2)
        self._econ_set_4 = self._econ_set_1.intersection(self._econ_set_2)
        print("El diccionario {0} tiene un total de {1} palabras.".format(1,len(self._econ_set_1)))
        print("El diccionario {0} tiene un total de {1} palabras.".format(2,len(self._econ_set_2)))
        print("El diccionario {0} tiene un total de {1} palabras.".format(3,len(self._econ_set_3)))
        print("El diccionario {0} tiene un total de {1} palabras.".format(4,len(self._econ_set_4)))

        writer = open("../db/H4Lvd_Dictionary/MyEconomicTerms.txt", "w")
        for term in self._econ_set_4:
            writer.write("{0}\n".format(term))
        writer.close()
        self._diccionarioEconomico = self._econ_set_4

            #if any(x  in diccionario[palabra] for x in self._RELATED_TO_ECONOMICS):
            #    self._diccionarioEconomico.add(palabra)
        #print("Cantidad de palabras en el diccionario de economia: {0}".format(str(len(self._diccionarioEconomico))))


    def _countEconomicTerms(self,document):
        count = 0
        for terminoEconomico in self._diccionarioEconomico:
            if terminoEconomico in document.words:
                count += int(document.words[terminoEconomico])
        return count

    def sortByEconomicRelevance(self, listOfDocuments):
        sortedList = [(doc,self._countEconomicTerms(doc)) for doc in listOfDocuments]
        sortedList.sort(key=lambda x : x[1], reverse=True)
        return [elem[0] for elem in sortedList]

    def funcEconomicRelevance(self,listOfDocuments):
        list = [(doc,self._countEconomicTerms(doc)) for doc in listOfDocuments]
        maxNro = max([count for (document,count) in list])
        resultado_funcion = [float(count)/float(maxNro) for (document,count) in list]
        return resultado_funcion



    def isEconomic(self, document):
        for word in self._diccionarioEconomico:
            if word in document.words:
                return True
        return False
