from bs4 import BeautifulSoup
import requests
import nltk
from nltk.stem import WordNetLemmatizer
import itertools

neurowords = set()
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
wordnet_lemmatizer = WordNetLemmatizer()

# Erm, copyright? erm?
url = u'https://www.ncbi.nlm.nih.gov/books/NBK10981/'
# We want the <dt></dt> bits
soup = BeautifulSoup(requests.get(url).text, "html.parser")
# Get all dt
terms=[nltk.word_tokenize(t.text) for t in soup("dt")]
merged = list(itertools.chain(*terms))
for w in merged:
    if w.isalpha() and len(w) > 2:
        neurowords.add(wordnet_lemmatizer.lemmatize(w))
# 763!

neurowords = neurowords - english_vocab
# 165 after removing common words

with open('neuroscience.txt', 'w') as file_handler:
    for item in neurowords:
        status = file_handler.write("{}\n".format(item))
