#!/usr/bin/python3

# filtrar por pais:



# clean libras
PATTTERN_LIBRAS = '£[0-9]+'
import re
def remove_libras(list_of_tokens):
    return [elem for elem in list_of_tokens if  re.search(PATTTERN_LIBRAS,elem)== None  ]

# eliminar apostrofe
def remove_apostrofes(tokens):
    return [elem for elem in tokens if not elem.startswith("\'")]

# Clean html
from bs4 import BeautifulSoup
def clean_html(text):
    return BeautifulSoup(text).get_text()

# Filtrar stopwords
from nltk.corpus import stopwords
def remove_stopwords(tokenized_text):
    return [palabra for palabra in tokenized_text if not palabra in stopwords.words('english')]

# Eliminar signos de puntuacion
import string
def remove_punctuation(list_of_tokens):
    return [palabra for palabra in list_of_tokens if not palabra in string.punctuation]

#stemming -- The WordNet lemmatizer only removes affixes if the resulting word is in its dictionary.
import nltk
wnl = nltk.WordNetLemmatizer()
def stemming(list_of_tokens):
    return [wnl.lemmatize(t) for t in list_of_tokens]


def my_tokenizer(raw):
    text = raw.lower()
    text = clean_html(text)
    tokens = nltk.word_tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = remove_punctuation(tokens)
    tokens = remove_libras(tokens)
    tokens = remove_apostrofes(tokens)
    tokens = stemming(tokens)
    return tokens
#
# Falta Entity Recognition < --------------------------
#

# Todo a lower
# eliminar html
# Aplicacion de entity recognition
# eliminar stopwords
# eliminar signos de puntuacion y numeros (4m libras)
# stemming
