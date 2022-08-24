from pathlib import Path
from typing import List

try:
    import yaml
except (NameError, ModuleNotFoundError):
    import sys
    print('PyYAML is needed for this game.')
    raise ImportError(
        'PyYAML is needed for this game.\n' +
        f'Install it: {sys.executable} -m pip install PyYAML',
    )


chars = 2 # characters to play with, ideally 2
words_file = 'words.yaml'
debug = False


def write_words(words) -> None:
    with open(words_file, 'w') as stream:
        yaml.dump(words, stream)


def main() -> int:
    if Path(words_file).is_file():
        with open(words_file, 'r') as stream:
            try:
                word_definitions = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(f"File {words_file} doesn't exist.")
        return 1
    words: List[str]
    words = word_definitions[:]
    if debug:
        print(words)
    print('zacni nejakym slovem')
    played_words: List[str] = []
    while True:
        # players's turn
        while True:
            if debug:
                print(f'{words=}')
                print(f'{played_words=}')
            word = input('>> ').lower()
            if word in ['q']:
                write_words(words)
                return 0
            if len(word) < 2:
                print('musis zadat slovo, ktere ma aspon 2 znaky')
            else:
                if len(played_words) == 0:
                    played_words.append(word)
                    break
                if word in played_words:
                    print('toto slovo uz bylo hadano')
                else:
                    if (len(played_words) > 0) and (played_words[-1][-chars:] == word[:chars]):
                        break
                    else:
                        print('spatne navazujici slovo')
                        print(f'rikal jsem: {w}')
                        if word not in words:
                            words.append(word)

        if word not in words:
            words.append(word)
        else:
            if word not in played_words:
                played_words.append(word)

        # computer's turn
        remaining_words = set(words) - set(played_words)
        if len(remaining_words) > 0:
            if debug:
                print(f'{remaining_words=}')
                print(f'{word}')
            ok = False
            for w in remaining_words:
                if word[-chars:] == w[:chars]:
                    ok = True
                    break
            if ok:
                played_words.append(w)
                print(w)
            else:
                print('Nevim. Vyhrals.')
                write_words(words)
                return 0
        else:
            print('Neznam zadna dalsi slova. Vyhrals.')
            write_words(words)
            return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
