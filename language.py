import sys


class Language:
    def __init__(self, language: str) -> None:
        self.language = language
        if language == 'en':
            self.import_error = 'PyYAML is needed for this game.\n' +\
                f'Install it: {sys.executable} -m pip install PyYAML'
            self.pyyaml_needed = 'PyYAML is needed for this game.'
            self.controls = 'controls:'
            self.quit_instruction = '"q" will quit the game'
            self.dunno_instruction = 'if you write "dunno", you ' +\
                'give yo the game and we can play again'
            self.one_letter_instruction = 'guess words starting ' +\
                'with the same letter as the last letter of previous word',
            self.start_guessing = 'start with some word'
            self.i_won = 'I won! :)'
            self.word_too_short = 'the word must have at least 2 characters'
            self.one_word_only = 'enter only one word. not more.'
            self.already_guessed = 'this word was already used. try another.'
            self.wrong_word = 'word not starting according to the rules'
            self.you_won = 'I give up. You won!'
            self.yaml_dict = 'yaml dictionary file'
            self.play_again = 'Play again? (y/n)'

        else:  # default language is cs
            self.import_error = 'PyYAML je potreba pro tuto hru.\n' +\
                f'Nainstaluj ho: {sys.executable} -m pip install PyYAML'
            self.pyyaml_needed = 'PyYAML je potreba pro tuto hru.'
            self.controls = 'ovladani:'
            self.quit_instruction = '"q" ukonci hru a vrati te zpet do konzole'
            self.dunno_instruction = 'kdyz napises "nevim", tak ' +\
                'vzdas aktualni hru a muzeme hrat znovu'
            self.one_letter_instruction = 'hadaji se slova, ktere zacinaji ' +\
                'na posledni pismeno slova predchoziho',
            self.start_guessing = 'zacni nejakym slovem'
            self.i_won = 'vyhral jsem! :)'
            self.word_too_short = 'musis zadat slovo, ktere ma aspon 2 znaky'
            self.one_word_only = 'musis zadat jen jedno slovo. ne vice.'
            self.already_guessed = 'toto slovo uz bylo hadano. zkus jine.'
            self.wrong_word = 'spatne navazujici slovo'
            self.you_won = 'Nevim. Vyhrals.'
            self.yaml_dict = 'yaml slovnik'
            self.play_again = 'Chces hrat znovu? (y/n)'

    def i_know_words(self, n: int) -> str:
        if self.language == 'en':
            return f'I know {n} words :)'
        else:
            return f'uz znam {n} slov :)'

    def more_letter_instruction(self, n: int) -> str:
        if self.language == 'en':
            return f'guess words starting with the same {n} letters ' +\
                f'as the last {n} letters of the previous word'
        else:
            return 'hadaji se slova, ktere zacinaji ' +\
                f'na posledni {n} pismena slova predchoziho'
