__author__ = 'IrinaPavlova'
import urllib.request as urlr
import re, bz2
import pandas as pd


my_dic = pd.read_excel('ISO 639-2.xlsx', header=None, index_col=1).to_dict()
language_codes = my_dic[0]
language_codes = dict((k.lower(), v.lower()) for k, v in language_codes.items())


def langcode():
    dictionary = language_codes
    name = input('Enter the language: ').lower()
    try:
        lang_code = dictionary[str(name)]
        print('We process... Please wait.')
        return lang_code
    except KeyError:
        return None


def makepage():
    try:
        global lang_code
        lang_code = langcode()
        page = urlr.urlopen('https://dumps.wikimedia.org/' + lang_code + 'wiki/latest')
        page_r = page.read().decode('utf-8')
        page_l = page_r.split('\n')
        return page_l, lang_code
    except TypeError:
        pass



def makeadr():
    try:
        global adr, title
        page_l = makepage()[0]
        s = re.compile('.*latest-pages-articles\.xml\.bz2')
        for line in page_l:
            if s.search(line) == None:
                pass
            else:
                title = re.search('>(.*?)<', line).group(1)
                adr = 'https://dumps.wikimedia.org/' + lang_code + 'wiki/latest/' + title
                break
        return adr, title
    except TypeError:
        pass


def retrieve():
    urlr.urlretrieve(adr, title)
    archive = bz2.BZ2File(title)
    archived = archive.read()
    xml_file = title[0:-4]
    open(xml_file, 'wb').write(archived)


def load_dump():
    makeadr()
    try:
        check = urlr.urlopen(adr)
        if int(check.info()['Content-Length']) > 50000000:
            decision = input('Are you sure you want to download the file? ')
            if decision.lower() == 'yes':
                retrieve()
            else:
                print('You decided to stop the download.')
        else:
            retrieve()
    except NameError:
        print('\nSorry, it is not a valid language name.')


def find_articles():
    articles = open('article_names.txt', 'w')
    arr = []
    xml_file = open(title[0:-4], 'r')
    for line in xml_file:
        m = re.search('<title>(.*?)</title>', line)
        if m != None:
            article = str(m)
            arr.append(article)

    narr = []
    for h in arr:
        k = re.search('title>(.*?)</', h)
        if k != None:
            narr.append(k.group(1))
    narr.sort()
    for l in narr: articles.write(l+'\n')
    articles.close()

load_dump()
find_articles()


