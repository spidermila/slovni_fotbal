from dbmanager import DBManager


class Users:
    def __init__(self) -> None:
        self.dbm = DBManager()

    def add_user(self, user_name: str) -> None:
        if not self.dbm.user_in_db(user_name):
            self.dbm.add_user(user_name)

    def add_game(
        self,
        user_name: str,
        user_guessed_count: int,
        game_guessed_count: int,
        user_won: bool,
    ) -> None:
        self.dbm.add_game(
            user_name,
            user_guessed_count,
            game_guessed_count,
            user_won,
        )

    def get_game_stats(self, user_name: str) -> tuple[int, int]:
        return self.dbm.get_game_stats_by_user(user_name)
