# slovni_fotbal
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/spidermila/slovni_fotbal/main.svg)](https://results.pre-commit.ci/latest/github/spidermila/slovni_fotbal/main)

A simple text based game of Word Soccer. Another of my wee projects made simply to learn Python. This version of the game stores data in sqllite database via sqlalchemy.

The game learns new words as you play . It will use the words against you in the next plays. So don't use made up words, cause it will eventually backfire :)

run:
```
python sf.py
```

You can chose how many letters of the previous word have to match the first letters of the next word by the ``-c, --chars`` argument. Default is 2. I recommend using value of 1 for feeding the dictionary or simpler gameplay - for kids. For example:
```
python sf.py -c 1
```

Default language is ``cs`` (Czech).

For English, you can run:
```
python sf.py -l en
```

Enjoy!
