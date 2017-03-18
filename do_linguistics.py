from bs4 import BeautifulSoup
import requests
import nltk
import itertools
import hunspell

hobj = hunspell.HunSpell('en_US.dic', 'en_US.aff')

domain_terms = set()
# english_vocab = set(w.lower() for w in nltk.corpus.words.words())

def extract_tags(url, tag):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    terms=[nltk.word_tokenize(t.text) for t in soup(tag)]
    merged = list(itertools.chain(*terms))
    return set([ (w.lower() if w.istitle() else w) for w in merged if w.isalpha() and len(w) > 2 and not(w.isupper()) and not(hobj.spell(w) or hobj.spell(w.lower())) ])

# Erm, copyright? erm?
# not much "out of English vocab" words
url = u'http://www.cs.bham.ac.uk/~pxc/nlp/nlpgloss.html'
# We want the <dt></dt> bits
domain_terms.update(extract_tags(url, u'strong'))

# ditto re the copyright
url = 'https://www.uni-due.de/ELE/LinguisticGlossary.html'
domain_terms.update(extract_tags(url, u'b'))

# Remove common English words—at least, according to nltk
# (Might be better to compare against hunspell instead but I dunno how)
# domain_terms = domain_terms - english_vocab

with open('linguistics-en.txt', 'w') as file_handler:
    for item in sorted(domain_terms):
        status = file_handler.write("{}\n".format(item))
