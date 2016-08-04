# Language Model
[![GitHub license](https://img.shields.io/pypi/l/pyzipcode-cli.svg)](https://img.shields.io/pypi/l/pyzipcode-cli.svg) [![Supported python versions](https://img.shields.io/pypi/pyversions/Django.svg)]([![PyPI](https://img.shields.io/pypi/pyversions/Django.svg)]())

A simple Language model having features such as **Autocomplete, Spell Check, Word Segmenter, Custom Entity Tagger, Nearest Words**.

## Index
- [Features](#features) 
- [Installation](#installation)
    - [Clone it](#clone-it)
    - [Run it](#run-it)
- [How To Use ??](#how-to-use??)
- [Issues](#issues)

## Features
[:arrow_up: Back to top](#index)

- **Autocomplete** : predict the future words/sentences on the basis of given words/letters.
- **Spell Check** : Returns the correct candididates word for the entered wrong word.
- **Entity Tagger** : Returns the entities in a given correct or disambiguated query, along with the domains to which they belongs.
- **Word Segmenter** : Returns the segmented words from given joined query/sentence.
- **Nearest words** :Returns the nearest words to the given word.

## Installation
[:arrow_up: Back to top](#index)

#### Clone it


```sh
$ git clone https://github.com/codeorbit/Language_Model
$ cd Language_Model && pip install -r requirements.txt
```

#### Run it

Fire it up! :volcano:
```sh
$ python api.py
```
## How To Use??

Created api calls for each features which returns result as json.
- **List of api** : Request `http://localhost:7777/language_model/` 
    - **Result** : will show all api call urls.

- **Autocomplete** : Request `http://localhost:7777/language_model/autocomplete/<name>` where `name` will be word/sentence/letter (without angle brackets).
    - **Result** : list of words or sentences which can come after the given word/sentence/letter in decreasing order of their probability.

- **Spell Check** : Request `http://localhost:7777/language_model/spellcheck/<name>` where `name` will be incorrect word (wihtout angle brackets).
    - **Result** : list of correct candidate words for entered incorrect word.

- **Word Segmenter** : Request `http://localhost:7777/language_model/wordsegment/<name>` where `name` will be joined words or sentences (without angle brackets) for e.g. `googlegmail` .
    - **Result** : Returns the list of segmented words for e.g. `[google,gmail]`.

- **Entity Tagger** : Request `http://localhost:7777/language_model/getentity/<name>` where `name` will be sentences or words after removing stopwords.
    - **Result** : Returns given query, tagged entities, and their domains and disambiguation link.

- **Nearest Words** : Request `http://localhost:7777/language_model/nearestword/<name>` where `name` will be word for which nearest needs to be find.
    - **Result** : Returns list of top 5 nearest words.
    - **Alternate** : Request `http://localhost:7777/language_model/nearestword/<name>/<top_n>` where `top_n` will be integer. This will return `top_n` nearest results.  


## Issues

You can [tweet me](https://twitter.com/decoding_life) if you can't get it to work. In fact, you should tweet me anyway.
