import os
import sys

from libs.game import Game
from libs.language import Language


class Cli:
    def __init__(self, lang_code: str = 'cs', chars: int = 2) -> None:
        self.lang = Language(lang_code)
        self.game = Game(self.lang, chars)

    def clear(self) -> None:
        if sys.platform.find('win') != -1:
            os.system('cls')
        else:
            os.system('clear')

    def myprint(self, s: str) -> None:
        print(s)

    def myinput(self, prompt: str = '>> ') -> str:
        return input(prompt)

    def run(self) -> int:
        self.clear()
        row_len = 0
        if len(self.game.user_names) > 0:
            print(f'{self.lang.users}: ')
            for row in self.lang.user_stats(
                self.game.users.get_all_game_stats(),
            ):
                if row_len < len(row):
                    row_len = len(row)
                print(row)

        print('-' * row_len)
        while True:
            uname = input(f'{self.lang.your_name}: ')
            if len(uname) < 3:
                if uname in ('Q', 'q'):
                    return 0
                print(self.lang.name_too_short)
            else:
                if uname not in self.game.user_names:
                    for existing_uname in self.game.user_names:
                        if uname.lower() == existing_uname.lower():
                            while True:
                                print(
                                    f'{self.lang.did_you_mean} {existing_uname}? (y/n)',  # noqa: E501
                                )
                                answer = input('> ')
                                if answer.lower() == 'y' or answer == '':
                                    uname = existing_uname
                                    break
                                elif answer.lower() == 'n':
                                    break
                                else:
                                    print(self.lang.answer_yn)
                self.game.users.active_user_name = uname
                self.game.users.add_user(self.game.users.active_user_name)
                break

        while True:
            print('-' * row_len)
            rc = self.game.play(self.myinput, self.myprint)
            if rc == 1:
                break
            while True:
                print(self.lang.play_again)
                answer = input('> ')
                if answer in ('Y', 'y'):
                    if len(self.game.user_names) > 0:
                        print(f'{self.lang.users}: ')
                        for row in self.lang.user_stats(
                            self.game.users.get_all_game_stats(),
                        ):
                            print(row)
                        print('-' * 20)
                    break
                elif answer in ('N', 'n'):
                    return 0
                else:
                    print(self.lang.answer_yn)
        return 0
