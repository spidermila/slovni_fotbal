from dbmanager import DBManager


class Words:
    def __init__(self) -> None:
        # self.words: list[str] = []
        self.dbm = DBManager()
        # initial fetch of words from DB

    def count(self) -> int:
        return self.dbm.word_count()

    def add_word(self, word: str) -> None:
        if not self.dbm.word_in_db(word):
            self.dbm.add_word(word)
        else:
            pass
            # print(f'word {word} already in db')

    def word_exists(self, word: str) -> bool:
        return self.dbm.word_in_db(word)

    def count_without_some(self, some: set[str]) -> int:
        return self.dbm.word_count_without_some(some)

    def get_all(self) -> list:
        return self.dbm.get_all_words()

    def get_words_without_some(self, some: set[str]) -> list:
        return self.dbm.get_words_without_some(some)
