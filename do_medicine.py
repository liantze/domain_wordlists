#!/usr/bin/env python
# important notice of source, in appliance with the NLM's® GENERAL TERMS
# AND CONDITIONS
"""
Downloads a list of `MeSH®`-terms, as created by
`NLM®<https://www.nlm.nih.gov/databases/download/terms_and_conditions_mesh.html>`_
from their website and parses it into a wordlist.
"""
import datetime

import nltk
import hunspell
import urllib

# On first use I needed to include this after installin nltk
# nltk.download("punkt")


hobj = hunspell.HunSpell("en_US.dic", "en_US.aff")


def extract_tags(line):
    def in_hunspell(w):
        return not (hobj.spell(w) or hobj.spell(w.lower()))

    terms = nltk.word_tokenize(line)
    return set(
        [
            (w.lower() if w.istitle() else w)
            for w in terms
            if w.isalpha()
            and len(w) > 2
            and not (w.isupper())
            and in_hunspell(w)
        ]
    )


def parser_ascii(file_):
    for line in file_:
        line = line.decode()

        if line.startswith("MH = "):
            yield line[len("MH = ") :]

MESH_URL_TEMPLATE = (
    "ftp://nlmpubs.nlm.nih.gov/online/mesh/MESH_FILES/asciimesh/d{year}.bin"
)

def main():
    terms = set()

    # Starting one year into the future since apparently they delete the files
    # of the current year towards the end of it
    year = datetime.date.today().year + 1

    while True:
        # That year should exist at least.
        if year >= 2018:
            try:
                url = MESH_URL_TEMPLATE.format(year=year)
                print("== Requesting URL: {}".format(url))
                with urllib.request.urlopen(url) as mesh_file:
                    print("== File downloaded, starting parsing ...")
                    for term in parser_ascii(mesh_file):
                        terms.update(extract_tags(term))

                print("== Parsed file, checking whether there is a previous "
                      "version ....")
            except urllib.error.URLError:
                print("== Couldn't get file, trying one year before ...")

            year -= 1
        else:
            if not terms:
                raise Exception("Somethings wrong, maybe the base url changed?")
            else:
                print("== Arrived at 2018, there shouldn't be older files.")
            break

    wordlist_file_name = "medicine-en.txt"
    print("== Writing wordlist to: {}".format(wordlist_file_name))

    with open(wordlist_file_name, "w") as wordlist_file:
        for item in sorted(terms):
            status = wordlist_file.write("{}\n".format(item))


if __name__ == "__main__":
    main()
