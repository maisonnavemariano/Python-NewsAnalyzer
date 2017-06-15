from collections import defaultdict

print(' -- CLASE IMPORTADA --')
_cjto_palabras = set()
_index_to_word = {}
_cantidad = 0

# _init = True
class wordvector(object):
    def __init__(self, _list_of_words):
        for word in _list_of_words:
            if not word in _cjto_palabras:
                _cjto_palabras.add(word)
                _index_to_word[_cantidad] = word
                _cantidad += 1
        self.values = defaultdict(int)
        print('init object with: '+str(_list_of_words))
        # if not _init:
        #     print('[WARNING] La clase wordvector debe ser importada junto con todo el modulo.')
