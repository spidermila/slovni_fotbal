class Language:
    '''\
        Language class. Default language is 'cs'
    '''
    def __init__(self, language: str) -> None:
        allowed_languages = ('cs', 'en', 'es')
        if language not in allowed_languages:
            raise ValueError(f'Wrong language selected! {allowed_languages=}')
        self.language = language

        if language == 'en':
            self.answer_yn = 'Answer "Y/y" for yes or "N/n" for no.'
            self.users = 'Users'
            self.your_name = 'Your name'
            self.name_too_short = 'Name must be longer than 3 characters!'
            self.did_you_mean = 'Did you mean'
            self.controls = 'controls:'
            self.quit_instruction = '"q" will quit the game'
            self.dunno = 'dunno'
            self.dunno_instruction = f'if you write "{self.dunno}", you ' +\
                'give yo the game and we can play again'
            self.one_letter_instruction = (
                'guess words starting ' +
                'with the same letter as the last letter of previous word'
            )
            self.start_guessing = 'start with some word'
            self.i_won = 'I won! :)'
            self.word_too_short = 'the word must have at least 2 characters'
            self.one_word_only = 'enter only one word. not more.'
            self.already_guessed = 'this word was already used. try another.'
            self.wrong_word = 'word not starting according to the rules'
            self.i_said = 'I said'
            self.you_won = 'I give up. You won!'
            self.play_again = 'Play again? (y/n)'

        elif language == 'es':
            self.answer_yn = 'Responda "Y/y" para sí o "N/n" para no.'
            self.users = 'Jugadores'
            self.your_name = 'Tu nombre'
            self.name_too_short = 'El nombre tiene debe ser mas largo ' +\
                'que 3 caracteres!'
            self.did_you_mean = 'Quisiste decir'
            self.controls = 'Instrucciones:'
            self.quit_instruction = '"q" te hará salir del juego'
            self.dunno = 'no sé'
            self.dunno_instruction = f'si escribes "{self.dunno}", te ' +\
                'rindes y el juego termina.'
            self.one_letter_instruction = (
                'Adivina palabras que comienzan con la misma ' +
                'letra como la última letra de la palabra anterior.'
            )
            self.start_guessing = 'comienza escribiendo una palabra'
            self.i_won = 'Yo gané! :)'
            self.word_too_short = 'la palabra debe tener al menos 2 caracteres'
            self.one_word_only = 'escibe una sola palabra. no mas.'
            self.already_guessed = 'esta palabra ya se usó. intenta con otra.'
            self.wrong_word = 'la palabra no comienza con la letra, ' +\
                'de acuerdo a las reglas'
            self.i_said = 'Dije'
            self.you_won = 'Me rindo. Tu ganas!'
            self.play_again = 'Quieres jugar otra vez? (y/n)'

        else:  # default language is cs
            self.answer_yn = 'Odpověz "Y/y" pro ano, nebo "N/n" pro ne.'
            self.users = 'Uživatelé'
            self.your_name = 'Tvoje jméno'
            self.name_too_short = 'Jméno musí být delší než 3 znaky!'
            self.did_you_mean = 'Měls namysli'
            self.controls = 'ovládání:'
            self.quit_instruction = '"q" ukončí hru'
            self.dunno = 'nevim'
            self.dunno_instruction = f'Když napíšeš "{self.dunno}", tak ' +\
                'vzdáš aktuální hru a můžeme hrát znovu'
            self.one_letter_instruction = (
                'hádají se slova, které začínají ' +
                'na poslední písmeno slova předchozího.'
            )
            self.start_guessing = 'Začni nejakým slovem.'
            self.i_won = 'Vyhrál jsem! :)'
            self.word_too_short = 'Musíš zadat slovo, které má aspoň 2 znaky.'
            self.one_word_only = 'Musíš zadat jen jedno slovo, ne více.'
            self.already_guessed = 'Toto slovo už bylo hádáno. Zkus jiné.'
            self.wrong_word = 'Špatně navazujíci slovo!'
            self.i_said = 'Říkal jsem'
            self.you_won = 'Nevím. Vyhráls.'
            self.play_again = 'Chceš hrát znovu? (y/n)'

    def i_know_words(self, n: int) -> str:
        if self.language == 'en':
            return f'I know {n} words :)'
        elif self.language == 'es':
            return f'Ya sé {n} palabra(s) :)'
        else:
            return f'Už znám {n} slov :)'

    def more_letter_instruction(self, n: int) -> str:
        if self.language == 'en':
            return f'Guess words starting with the same {n} letters ' +\
                f'as the last {n} letters of the previous word.'
        elif self.language == 'es':
            return f'Adivina palabras que comienzan con las mismas {n} ' +\
                f'letras como las últimas {n} letras de la palabra anterior.'
        else:
            return 'Hádají se slova, které začínají ' +\
                f'na poslední {n} pismena slova předchozího.'

    def user_stats(self, stat_dict: dict[str, tuple[int, int]]) -> list[str]:
        max_uname = 0
        max_won = 0
        max_lost = 0
        for uname, stats in stat_dict.items():
            won, lost = stats
            if len(uname) > max_uname:
                max_uname = len(uname)
            if len(str(won)) > max_won:
                max_won = len(str(won))
            if len(str(lost)) > max_lost:
                max_won = len(str(lost))
        result = []
        if self.language == 'en':
            won_text = 'won'
            lost_text = 'lost'
        elif self.language == 'es':
            won_text = 'ganados'
            lost_text = 'perdidos'
        else:
            won_text = 'výhry'
            lost_text = 'prohry'
        for uname, stats in stat_dict.items():
            won, lost = stats
            result.append(
                f'{uname:<{max_uname}} - {won_text}: {won:<{max_won}}, '
                f'{lost_text}: {lost:<{max_lost}}',
            )
        return result
