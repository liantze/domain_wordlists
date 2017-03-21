from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

mathwords = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])

urls = [u'https://en.wikipedia.org/wiki/Glossary_of_biology'
        ]

for url in urls:
    mathwords.update(extract_tags(url, u'b'))

# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# mathwords = mathwords - english_vocab

with open('biology-en.txt', 'w') as file_handler:
    for item in sorted(mathwords):
        status = file_handler.write("{}\n".format(item))
