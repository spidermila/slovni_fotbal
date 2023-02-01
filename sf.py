import argparse

from language import Language
from words import Words


debug = False


def play(lang: Language, chars: int) -> int:
    words = Words()
    w: str = ''
    print(lang.i_know_words(words.count()))
    print(lang.controls)
    print(lang.quit_instruction)
    print(lang.dunno_instruction)
    if chars == 1:
        print(lang.one_letter_instruction)
    else:
        print(lang.more_letter_instruction(chars))
    print(lang.start_guessing)
    played_words: set[str] = set()
    while True:
        # players's turn
        while True:
            # if debug:
            #     print(f'{words=}')
            #     print(f'{played_words=}')
            word = input('>> ').lower()
            if word in ['q']:
                return 0
            if word in ['nevim', 'dunno']:
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
                        print(word)
                        words.add_word(word)

        words.add_word(word)
        played_words.add(word)

        # computer's turn
        if words.count_without_some(played_words) > 0:
            ok = False
            for w in words.get_words_without_some(played_words):
                if word[-chars:] == w[:chars]:
                    ok = True
                    break
            if ok:
                played_words.add(w)
                print(w)
            else:
                print(lang.you_won)
                return 0
        else:
            print(lang.you_won)
            return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-l',
        default='cs',
        type=str,
        help='language: cs or en',
    )
    parser.add_argument(
        '-c',
        '--chars',
        default='2',
        type=int,
        help='number of characters to match. default 2',
    )
    args = parser.parse_args()
    lang = Language(args.l)
    chars = args.chars

    lang.language

    while True:
        rc = play(lang, chars)
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
