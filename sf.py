import argparse
from pathlib import Path

try:
    import yaml
except (NameError, ModuleNotFoundError):
    import sys
    print('PyYAML is needed for this game.')
    raise ImportError(
        'PyYAML is needed for this game.\n' +
        f'Install it: {sys.executable} -m pip install PyYAML',
    )


chars = 2  # characters to play with, ideally 2
words_file = 'words.yaml'
debug = False


def write_words(w: set[str]) -> None:
    words = list(w)
    # words.sort()
    with open(words_file, 'w') as stream:
        yaml.dump(words, stream)


def play(words: set[str]) -> int:
    w: str = ''
    if debug:
        print(words)
    print(f'uz znam {len(words)} slov :)')
    print('zacni nejakym slovem')
    played_words: set[str] = set()
    # last_word: str = ''
    while True:
        # players's turn
        while True:
            if debug:
                print(f'{words=}')
                print(f'{played_words=}')
            word = input('>> ').lower()
            if word in ['q']:
                write_words(words)
                return 1
            if len(word) < 2:
                print('musis zadat slovo, ktere ma aspon 2 znaky')
            else:
                if len(played_words) == 0:
                    played_words.add(word)
                    # last_word = word
                    break
                if word in played_words:
                    print('toto slovo uz bylo hadano')
                else:
                    if (
                        (len(played_words) > 0) and
                        (w[-chars:] == word[:chars])
                    ):
                        break
                    else:
                        print('spatne navazujici slovo')
                        print(f'rikal jsem: {w}')
                        words.add(word)

        words.add(word)
        played_words.add(word)

        # computer's turn
        remaining_words = words - played_words
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
                played_words.add(w)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'soubor',
        nargs='?',
        default='words.yaml',
        type=str,
        help='yaml slovnik',
    )
    args = parser.parse_args()
    words_file = args.soubor
    if Path(words_file).is_file():
        with open(words_file, 'r') as stream:
            try:
                words = set(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)
    else:
        print(f"File {words_file} doesn't exist.")
        return 1
    while True:
        rc = play(words)
        if rc == 1:
            break
        while True:
            print('Chces hrat znovu? (y/n)')
            answer = input('> ')
            if answer in ('Y', 'y'):
                break
            elif answer in ('N', 'n'):
                return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
