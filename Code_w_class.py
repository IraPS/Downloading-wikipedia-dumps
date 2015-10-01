# Homework-2
__author__ = 'IrinaPavlova'

import re
import os
import bz2
import urllib.request as urlr
import xml.dom.minidom as xdm


class Dump(object):

    def __init__(self):
        self.name = ''
        self.languageCodes = {}
        self.langCode = ''
        self.page_l = ''
        self.dumpTitle = ''
        self.urlAdr = ''
        self.xmlFile = ''

    def open_csv(self):
        myDict = open('ISO 639-2.csv', 'r').readlines()
        for line in myDict:
            line = re.sub('\n', '', line).split(';')
            self.languageCodes[line[1].lower()] = line[0]

    def lang_code(self):
        dictionary = self.languageCodes
        self.name = input('Enter the language: ').lower()
        try:
            self.langCode = dictionary[self.name]
            print('We process... Please wait.')
        except KeyError:
            self.langCode = None

    def open_url(self):

        try:
            urlAdress = 'https://dumps.wikimedia.org/' + self.langCode + 'wiki/latest'
            page = urlr.urlopen(urlAdress)
            page_r = page.read().decode('utf-8')
            self.page_l = page_r.split('\n')
        except TypeError:
            pass

    def open_dump_url(self):
        try:
            s = re.compile('.*latest-pages-articles\.xml\.bz2')
            for line in self.page_l:
                if s.search(line) is None:
                    pass
                else:
                    self.dumpTitle = re.search('>(.*?)<', line).group(1)
                    self.urlAdr = 'https://dumps.wikimedia.org/' + self.langCode + 'wiki/latest/' + self.dumpTitle
                    print(self.urlAdr)
                    break
        except TypeError:
            pass

    def retrieve_dump(self):
        try:
            urlr.urlretrieve(self.urlAdr, self.dumpTitle)
            archive = bz2.BZ2File(self.dumpTitle)
            archived = archive.read()
            self.xmlFile = self.dumpTitle[0:-4]
            open(self.xmlFile, 'wb').write(archived)
        except ValueError:
            return None

    def load_dump(self):
        self.open_csv()
        self.lang_code()
        self.open_url()
        self.open_dump_url()

        try:
            check = urlr.urlopen(self.urlAdr)
            if int(check.info()['Content-Length']) > 6250000:
                decision = input('Are you sure you want to download the file? ')
                if decision.lower() == 'yes':
                    self.retrieve_dump()
                    print('\nThe dump is ready. Check the directory ' + os.path.realpath(dump.xmlFile))
                else:
                    print('You decided to stop the download.')
            else:
                self.retrieve_dump()
                print('\nThe dump is ready. Check the directory ' + os.path.realpath(dump.xmlFile))
        except ValueError:
            print('\nSorry, it is not a valid language name.')

    def find_articles(self):
        articles = open(self.name + '_article_names.txt', 'w')
        self.xmlFile = self.dumpTitle[0:-4]
        try:
            dom = xdm.parse(self.xmlFile)
            titles = []
            parsedTitles = dom.getElementsByTagName('title')
            for i in parsedTitles:
                title = (" ".join(t.nodeValue for t in i.childNodes if t.nodeType == t.TEXT_NODE))
                titles.append(title)
            titles.sort()
            for j in titles:
                articles.write(j + '\n')
            print('\nThe articles names are in the file ' + os.path.realpath(self.name + '_article_names.txt'))
        except FileNotFoundError:
            pass
        articles.close()


dump = Dump()
dump.load_dump()
dump.find_articles()

