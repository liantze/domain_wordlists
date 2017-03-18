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
    return set([ w for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])

### Mmmm these are nicely formatted as dt-dd
urls = [u'https://en.wikipedia.org/wiki/Glossary_of_algebraic_geometry',
        u'https://en.wikipedia.org/wiki/Glossary_of_category_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_commutative_algebra',
        u'https://en.wikipedia.org/wiki/Glossary_of_game_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_arithmetic_and_diophantine_geometry',
        u'https://en.wikipedia.org/wiki/Glossary_of_algebraic_topology',
        u'https://en.wikipedia.org/wiki/Glossary_of_classical_algebraic_geometry',
        u'https://en.wikipedia.org/wiki/Glossary_of_Principia_Mathematica',
        u'https://en.wikipedia.org/wiki/Glossary_of_set_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_graph_theory_terms',
        u'https://en.wikipedia.org/wiki/Glossary_of_invariant_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_Lie_algebras',
        u'https://en.wikipedia.org/wiki/Glossary_of_module_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_probability_and_statistics',
        u'https://en.wikipedia.org/wiki/Glossary_of_ring_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_string_theory',
        u'https://en.wikipedia.org/wiki/Glossary_of_tensor_theory',
        ]
# We want the <dt></dt> bits
for url in urls:
    mathwords.update(extract_tags(url, u'dt'))

# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# mathwords = mathwords - english_vocab

with open('maths-en.txt', 'w') as file_handler:
    for item in sorted(mathwords):
        status = file_handler.write("{}\n".format(item))
