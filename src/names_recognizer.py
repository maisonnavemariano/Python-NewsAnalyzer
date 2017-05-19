#!/usr/bin/python3
# leemos archivo nombres nltk:

    # >>> names = nltk.corpus.names
    #>>> names.fileids()
    #['female.txt', 'male.txt']
    # >>> male_names = names.words('male.txt')
    # >>> female_names = names.words('female.txt')
    # >>> [w for w in male_names if w in female_names]
    # ['Abbey', 'Abbie', 'Abby', 'Addie', 'Adrian', 'Adrien', 'Ajay', 'Alex', 'Alexis',
    # 'Alfie', 'Ali', 'Alix', 'Allie', 'Allyn', 'Andie', 'Andrea', 'Andy', 'Angel',
    # 'Angie', 'Ariel', 'Ashley', 'Aubrey', 'Augustine', 'Austin', 'Averil', ...]

# armarmos bigramas, si primer elemento del bigrama es noombre, y es un bigrama frecuente. Es nombre de persona?