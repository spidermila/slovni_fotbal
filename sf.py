import argparse
import os
import sys
from random import choice

from language import Language
from users import Users
from words import Words

debug = False

# TODO: chose from multiple word DBs - maybe one per language?


def clear() -> None:
    if sys.platform.find('win') != -1:
        os.system('cls')
    else:
        os.system('clear')


def play(lang: Language, chars: int, users: Users) -> int:
    user_guessed_count = 0
    game_guessed_count = 0
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
                return 1
            if word in ['nevim', 'dunno']:
                print(lang.i_won)
                users.add_game(
                    users.active_user_name,
                    user_guessed_count,
                    game_guessed_count,
                    False,
                )
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
                    if len(played_words) > 0:
                        if lang.language == 'cs' and 'ch' in w[-chars - 1:]:
                            if w[-chars - 1:] == word[:chars + 1]:
                                break
                        elif 'ch' in word[:chars + 1]:
                            print(f'{lang.wrong_word} - {word}')
                            print(lang.i_said, w)
                        elif w[-chars:] == word[:chars]:
                            break
                        else:
                            print(f'{lang.wrong_word} - {word}')
                            print(lang.i_said, w)

        words.add_word(word)
        played_words.add(word)
        user_guessed_count += 1

        # computer's turn
        if words.count_without_some(played_words) > 0:
            valid_answers = []
            for w in words.get_words_without_some(played_words):
                if lang.language == 'cs' and 'ch' in word[-chars - 1:]:
                    if word[-chars - 1:] == w[:chars + 1]:
                        valid_answers.append(w)
                elif word[-chars:] == w[:chars] and 'ch' not in w[:chars + 1]:
                    valid_answers.append(w)

            if len(valid_answers) > 0:
                w = choice(valid_answers)
                print(f'{valid_answers=}')
                played_words.add(w)
                game_guessed_count += 1
                print(w)
            else:
                print(lang.you_won)
                users.add_game(
                    users.active_user_name,
                    user_guessed_count,
                    game_guessed_count,
                    True,
                )
                return 0
        else:
            print(lang.you_won)
            users.add_game(
                users.active_user_name,
                user_guessed_count,
                game_guessed_count,
                True,
            )
            return 0


def main() -> int:
    clear()
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

    users = Users()
    user_names = users.get_user_names()
    row_len = 0
    if len(user_names) > 0:
        print(f'{lang.users}: ')
        for row in lang.user_stats(users.get_all_game_stats()):
            if row_len < len(row):
                row_len = len(row)
            print(row)

    print('-' * row_len)
    while True:
        uname = input(f'{lang.your_name}: ')
        if len(uname) < 3:
            if uname in ('Q', 'q'):
                return 0
            print(lang.name_too_short)
        else:
            if uname not in user_names:
                for existing_uname in user_names:
                    if uname.lower() == existing_uname.lower():
                        while True:
                            print(
                                f'{lang.did_you_mean} {existing_uname}? (y/n)',
                            )
                            answer = input('> ')
                            if answer.lower() == 'y' or answer == '':
                                uname = existing_uname
                                break
                            elif answer.lower() == 'n':
                                break
                            else:
                                print(lang.answer_yn)
            users.active_user_name = uname
            users.add_user(users.active_user_name)
            break

    while True:
        print('-' * row_len)
        rc = play(lang, chars, users)
        if rc == 1:
            break
        while True:
            print(lang.play_again)
            answer = input('> ')
            if answer in ('Y', 'y'):
                if len(user_names) > 0:
                    print(f'{lang.users}: ')
                    for row in lang.user_stats(users.get_all_game_stats()):
                        print(row)
                    print('-' * 20)
                break
            elif answer in ('N', 'n'):
                return 0
            else:
                print(lang.answer_yn)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
