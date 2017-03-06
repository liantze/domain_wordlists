## What this?

This started because of feedback from Overleaf users that the spell-checkers (straight from Ubuntu) were unsatisfactory, in that many domain-specific terms were missing. Users feel that LaTeX is widely used by mathematicians and scientists, and it's odd that the spell-checkers didn't respect that.

And to everyone's surprise although there has been many word lists (not even wordnets or thesauri, mind you!) for various languages, not to mention an abundance of research on keyword extraction, there doesn't seem to be any easy-to-use word lists for specific domains. Glossaries exist on the Web, but they need to be scraped.

And scrape them I will, if only because I'm getting tired of "Overleaf doesn't think my research field (neuroscience) is a real word" feedback. (Disclaimer: I was amused that the spell-checker didn't recognise many terms in *my* thesis!)

However each glossary list Web is formatted differently (as if that should be a surprise after I've been trying to process machine-readable dictionaries...), _including [Wikipedia glossary lists](https://en.wikipedia.org/wiki/Category:Wikipedia_glossaries)_, may even be  formatted differently. If we're lucky most of them will be formatted as `dt-dd` definition lists; but some may be formatted as tables or just marked with `<strong>` for the terms. I had hoped that Wikidata gives some respite, but it appears that the tuples have not been set up for most of these glossaries (see e.g. https://www.wikidata.org/wiki/Q5571762). So for now each script is rather ad-hoc! And perhaps badly coded because my coding-fu is rusty!

Also I have not figured out the copyright issues for these things, especially if they're not from Wikipedia/Wikidata.

## Domains
I started with neuroscience, because for some reason that field crops up a lot in Overleaf user feedback re the spell-checkers.

- Neuroscience: from https://www.ncbi.nlm.nih.gov/books/NBK10981/ (Copyright??)
- Linguistics and NLP (because that's my field :p)

## Translations

Theoretically speaking this is possible by leveraging Wikipedia/Wikidata queries, as I'd done a few times in the past. But I'll probably do that later. Much later.

## Proper integration into hunspell?

Probably with https://github.com/blatinier/pyhunspell? I have no idea how to do this yet (or whether I'll do it).
