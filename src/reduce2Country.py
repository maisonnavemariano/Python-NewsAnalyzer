#!/usr/bin/python3
import pickle
_country2code_file = '../db/pickle/map_country2code.p'
_country2code = pickle.load(open(_country2code_file,'rb'))

_news_file         = '../db/noticias/noticias2013'
_news_file_country = '../db/noticias/argentina/argentina2013'

_instanceNro_cons  = 'instanceNro: '
_title_cons        = 'webTitle: '
_section_cons      = 'sectionName: '
_headline_cons     = 'headline: '
_trailtext_cons    = 'trailText: '
_date_cons         = 'webPublicationDate: '
_bodytext_cons     = 'bodytext: '

_selected_country = 'argentina'
_allowed_sections = ["Society","Business","World news","Politics"]

noticias = []
news_text = open(_news_file,'r').read()
_noticias_procesadas = 0
for line in news_text.splitlines():
    if line.startswith(_instanceNro_cons):
        ins_nro = line[len(_instanceNro_cons):]

    if line.startswith(_title_cons):
        title = line[len(_title_cons):]

    if line.startswith(_section_cons):
        section = line [len(_section_cons):]

    if line.startswith(_headline_cons):
        headline = line[len(_headline_cons):]

    if line.startswith(_trailtext_cons):
        trailtext = line[len(_trailtext_cons):]

    if line.startswith(_date_cons):
        date = line[len(_date_cons):]

    if line.startswith(_bodytext_cons):
        body = line[len(_bodytext_cons):]

        if (_selected_country in body.lower() or _selected_country in _selected_country in title.lower()) and section in _allowed_sections:
            noticias.append((title,section, date, body))
            _noticias_procesadas += 1

writer = open(_news_file_country, 'w')
for noticia in noticias:
    writer.write(_title_cons    + noticia[0]  + '\n')
    writer.write(_section_cons  + noticia[1]  + '\n')
    writer.write(_date_cons     + noticia[2]  + '\n')
    writer.write(_bodytext_cons + noticia[3]  + '\n')
writer.close()

print('cantidad de noticias procesadas: {}'.format(_noticias_procesadas))
