def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

class Document(object):
    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ "

    def __init__(self, title, date=""):
        self.words = {}
        self.date = date
        self.title = "".join(c for c in title if c in self.PERMITTED_CHARS)

    def addText(self, text, stopwords):
        text = text.lower()
        text = "".join(c for c in text if c in self.PERMITTED_CHARS)
        words_array = text.split(" ")
        for word in words_array:
            if not word in stopwords and len(word) > 0 and not hasNumbers(word):
                if word in self.words:
                    self.words[word] = self.words[word] + 1
                else:
                    self.words[word] = 1