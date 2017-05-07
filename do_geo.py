from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

geowords = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])


def extract_list_items(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup.find(id="bodyContent")(u'li')]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])


urls = [
        ]

for url in urls:
    geowords.update(extract_list_items(url))


# With <dt>
urls = [
        ]

for url in urls:
    geowords.update(extract_tags(url, u'dt'))


# With <b>
urls = [b'https://en.wikipedia.org/wiki/Glossary_of_ecology',
        ]

for url in urls:
    geowords.update(extract_tags(url, u'b'))

# With <h2>
urls = [
        ]

for url in urls:
    geowords.update(extract_tags(url, u'h2'))

# With <td> siiigh
urls = [
        ]

for url in urls:
    geowords.update(extract_tags(url, u'td'))


# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# geowords = geowords - english_vocab

with open('geo-en.txt', 'w') as file_handler:
    for item in sorted(geowords):
        status = file_handler.write("{}\n".format(item))
