#!/usr/bin/python3

class Article(object):

    PERMITTED_CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"

    def __init__(self, title, sectionName='', headline='', trailtext='', bodyText='', date=''): #Default values '' if one of the parameters is not given.
        self.title       = title;
        self.sectionName = sectionName;
        self.headline    = headline;
        self.trailText   = trailtext;
        self.bodyText    = bodyText;
        self.date        = date;


    def isValidArticle(self):
        return len(self.bodyText)>0 and "".join(c for c in self.bodyText if c in self.PERMITTED_CHARS) ;

    def print(self):
        print(self.title + self.date );