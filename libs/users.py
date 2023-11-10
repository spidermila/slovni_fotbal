from libs.dbmanager import DBManager


class Users:
    def __init__(self) -> None:
        self.dbm = DBManager()
        self.active_user_name = ''

    def add_user(self, user_name: str) -> None:
        if not self.dbm.user_in_db(user_name):
            self.dbm.add_user(user_name)

    def get_user_names(self) -> list[str]:
        return self.dbm.get_user_names()

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

    def get_game_stats_for_user(self, user_name: str) -> tuple[int, int]:
        return self.dbm.get_game_stats_by_user(user_name)

    def get_all_game_stats(self) -> dict[str, tuple[int, int]]:
        return self.dbm.get_all_game_stats()
