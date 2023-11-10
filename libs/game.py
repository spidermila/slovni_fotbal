from random import choice
from typing import Callable

from libs.language import Language
from libs.users import Users
from libs.words import Words


class Game:
    def __init__(
        self,
        lang: Language,
        chars: int = 2,
    ) -> None:
        '''\
            lang - Language instance.
            chars - number of characters to match. default 2
        '''
        self.lang = lang
        self.chars = chars
        self.users = Users()
        self.user_names = self.users.get_user_names()
        self.words = Words()

    def play(
        self,
        callback_input: Callable[[], str],
        callback_output: Callable[[str], None],
    ) -> int:
        user_guessed_count = 0
        game_guessed_count = 0
        w = ''
        callback_output(self.lang.i_know_words(self.words.count()))
        callback_output(self.lang.controls)
        callback_output(self.lang.quit_instruction)
        callback_output(self.lang.dunno_instruction)
        if self.chars == 1:
            callback_output(self.lang.one_letter_instruction)
        else:
            callback_output(self.lang.more_letter_instruction(self.chars))
        callback_output(self.lang.start_guessing)
        played_words: set[str] = set()
        while True:
            # players's turn
            while True:
                word = callback_input().lower()
                if word in ['q']:
                    return 1
                if word == self.lang.dunno:
                    callback_output(self.lang.i_won)
                    self.users.add_game(
                        self.users.active_user_name,
                        user_guessed_count,
                        game_guessed_count,
                        False,
                    )
                    return 0
                if len(word) < 2:
                    callback_output(self.lang.word_too_short)
                elif len(word.split()) > 1:
                    callback_output(self.lang.one_word_only)
                else:
                    if len(played_words) == 0:
                        played_words.add(word)
                        break
                    if word in played_words:
                        callback_output(self.lang.already_guessed)
                    else:
                        if len(played_words) > 0:
                            if (
                                self.lang.language == 'cs' and
                                'ch' in w[-self.chars - 1:]
                            ):
                                if (
                                    w[-self.chars - 1:]
                                    == word[:self.chars + 1]
                                ):
                                    break
                            elif 'ch' in word[:self.chars + 1]:
                                callback_output(
                                    f'{self.lang.wrong_word} - {word}',
                                )
                                callback_output(f'{self.lang.i_said} {w}')
                            elif w[-self.chars:] == word[:self.chars]:
                                break
                            else:
                                callback_output(
                                    f'{self.lang.wrong_word} - {word}',
                                )
                                callback_output(f'{self.lang.i_said} {w}')

            self.words.add_word(word)
            played_words.add(word)
            user_guessed_count += 1

            # computer's turn
            if self.words.count_without_some(played_words) > 0:
                valid_answers = []
                for w in self.words.get_words_without_some(played_words):
                    if (
                        self.lang.language == 'cs' and
                        'ch' in word[-self.chars - 1:]
                    ):
                        if word[-self.chars - 1:] == w[:self.chars + 1]:
                            valid_answers.append(w)
                    elif (
                        word[-self.chars:] == w[:self.chars] and
                        'ch' not in w[:self.chars + 1]
                    ):
                        valid_answers.append(w)

                if len(valid_answers) > 0:
                    w = choice(valid_answers)
                    played_words.add(w)
                    game_guessed_count += 1
                    callback_output(w)
                else:
                    callback_output(self.lang.you_won)
                    self.users.add_game(
                        self.users.active_user_name,
                        user_guessed_count,
                        game_guessed_count,
                        True,
                    )
                    return 0
            else:
                callback_output(self.lang.you_won)
                self.users.add_game(
                    self.users.active_user_name,
                    user_guessed_count,
                    game_guessed_count,
                    True,
                )
                return 0
