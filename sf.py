import argparse
from pathlib import Path

from language import Language

# cs is the default language
# other languages: en
lang = Language('cs')

try:
    import yaml
except (NameError, ModuleNotFoundError):
    print(lang.pyyaml_needed)
    raise ImportError(lang.import_error)


words_file = ''
chars = 2  # characters to play with, ideally 2
debug = False


def read_words(words_file: str) -> set[str]:
    if Path(words_file).is_file():
        with open(words_file, 'r') as stream:
            try:
                words = set(yaml.safe_load(stream))
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError:
                # file is empty
                words = set()
    else:
        Path(words_file).touch()
        words = set()
    return words


def write_words(w: set[str], words_file: str) -> None:
    from_file = read_words(words_file)
    words = list(set(list(w) + list(from_file)))
    words.sort()
    with open(words_file, 'w') as stream:
        yaml.dump(words, stream)


def play(words: set[str], words_file: str) -> int:
    w: str = ''
    if debug:
        print(words)
    print(lang.i_know_words(len(words)))
    print(lang.controls)
    print(lang.quit_instruction)
    print(lang.dunno_instruction)
    if chars == 1:
        print(lang.one_letter_instruction)
    else:
        print(lang.more_letter_instruction(chars))
    print(lang.start_guessing)
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
                write_words(words, words_file)
                return 1
            if word in ['nevim', 'dunno']:
                write_words(words, words_file)
                print(lang.i_won)
                return 0
            if len(word) < 2:
                print(lang.word_too_short)
            elif len(word.split()) > 1:
                print(lang.one_word_only)
            else:
                if len(played_words) == 0:
                    played_words.add(word)
                    break
                if word in played_words:
                    print(lang.already_guessed)
                else:
                    if (
                        (len(played_words) > 0) and
                        (w[-chars:] == word[:chars])
                    ):
                        break
                    else:
                        print(lang.wrong_word)
                        print(w)
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
                print(lang.you_won)
                write_words(words, words_file)
                return 0
        else:
            print(lang.you_won)
            write_words(words, words_file)
            return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'soubor',
        nargs='?',
        default='words.yaml',
        type=str,
        help=lang.yaml_dict,
    )
    args = parser.parse_args()
    words_file = args.soubor
    words = read_words(words_file)

    while True:
        rc = play(words, words_file)
        if rc == 1:
            break
        while True:
            print(lang.play_again)
            answer = input('> ')
            if answer in ('Y', 'y'):
                break
            elif answer in ('N', 'n'):
                return 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
