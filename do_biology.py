from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

biowords = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])

# With <dt>
urls = [u'https://en.wikipedia.org/wiki/Glossary_of_ant_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_bird_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_phytopathology',
        u'https://en.wikipedia.org/wiki/Glossary_of_viticulture_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_entomology_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_invasion_biology_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_neuroanatomy',
        ]

for url in urls:
    biowords.update(extract_tags(url, u'dt'))


# With <b>
urls = [u'https://en.wikipedia.org/wiki/Glossary_of_biology',
        u'https://en.wikipedia.org/wiki/Glossary_of_arachnology_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_gene_expression_terms',
        ]

for url in urls:
    biowords.update(extract_tags(url, u'b'))

# With <h2>
urls = [u'https://en.wikipedia.org/wiki/Glossary_of_Asteraceae-related_terms',
        ]

for url in urls:
    biowords.update(extract_tags(url, u'h2'))

# With <td> siiigh
urls = [u'https://en.wikipedia.org/wiki/Glossary_of_leaf_morphology',
        u'https://en.wikipedia.org/wiki/Glossary_of_mammalian_dental_topography',
        ]

for url in urls:
    biowords.update(extract_tags(url, u'td'))


# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# biowords = biowords - english_vocab

with open('biology-en.txt', 'w') as file_handler:
    for item in sorted(biowords):
        status = file_handler.write("{}\n".format(item))
