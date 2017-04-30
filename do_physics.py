from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

physicswords = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])


def extract_wikipedia_cats(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup.find(id="bodyContent")(u'li')]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])


urls = [b'https://en.wikipedia.org/wiki/Category:Concepts_in_physics',
        b'https://en.wikipedia.org/wiki/Category:Mechanics',
        b'https://en.wikipedia.org/wiki/Category:Biomechanics',
        b'https://en.wikipedia.org/wiki/Category:Classical_mechanics',
]

for url in urls:
    physicswords.update(extract_wikipedia_cats(url))


# With <dt>
urls = [b'https://en.wikipedia.org/wiki/Glossary_of_elementary_quantum_mechanics',
        b'https://en.wikipedia.org/wiki/Glossary_of_quantum_philosophy',
        b'https://en.wikipedia.org/wiki/Glossary_of_string_theory',
        ]

for url in urls:
    physicswords.update(extract_tags(url, u'dt'))


# With <b>
urls = [b'https://en.wikipedia.org/wiki/Glossary_of_physics',
        b'https://en.wikipedia.org/wiki/Glossary_of_astronomy',
        b'https://en.wikipedia.org/wiki/Glossary_of_classical_physic',
        b'https://en.wikipedia.org/wiki/Glossary_of_meteoritics',
        ]

for url in urls:
    physicswords.update(extract_tags(url, u'b'))

# With <h2>
urls = [
        ]

for url in urls:
    physicswords.update(extract_tags(url, u'h2'))

# With <td> siiigh
urls = [
        ]

for url in urls:
    physicswords.update(extract_tags(url, u'td'))


# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# physicswords = physicswords - english_vocab

with open('physics-en.txt', 'w') as file_handler:
    for item in sorted(physicswords):
        status = file_handler.write("{}\n".format(item))
