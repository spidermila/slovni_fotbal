from libs.dbmanager import DBManager


def word_menu(dbm: DBManager) -> None:
    if len(dbm.get_all_words()) == 0:
        print('No words in the DB.')
        return
    while True:
        words = dbm.get_all_words()
        indexes = []
        for i, word in enumerate(words):
            indexes.append(str(i + 1))
            print(f'{i + 1}. {word}')
        print('-' * 20)
        print(
            '''\
            q - back
            d - delete
            ''',
        )
        cmd = input('> word menu (select command)> ')
        if cmd in ['Q', 'q', 'B', 'b']:
            break
        elif cmd == 'd':
            while True:
                word_number = input('Word number to delete: ')
                if word_number in ['Q', 'q', '']:
                    return
                if word_number in indexes:
                    break
                else:
                    print('Pick a word number from the list!')

            word = words[int(word_number) - 1]
            dbm.delete_word(word)


def user_menu(dbm: DBManager) -> None:
    if len(dbm.get_user_names()) == 0:
        print('No users in the DB.')
        return
    while True:
        unames = dbm.get_user_names()
        indexes = []
        for i, uname in enumerate(unames):
            indexes.append(str(i + 1))
            print(f'{i + 1}. {uname}')
        cmd = input('> user menu (select user) > ')
        if cmd in ['Q', 'q', 'B', 'b']:
            break
        elif cmd == 'h':
            print(
                '''\
            q / b - back
            [1-9] - select user
                ''',
            )
        elif cmd in indexes:
            uname = unames[int(cmd) - 1]
            user_selected(dbm, uname)


def user_selected(dbm: DBManager, uname: str) -> None:
    while True:
        cmd = input(f'> user menu ({uname}) > ')
        if cmd in ['Q', 'q', 'B', 'b']:
            break
        elif cmd == 'h':
            print(
                '''\
            q / b - back
            r - rename
            d - delete
            l - list games
                ''',
            )
        elif cmd in ['R', 'r']:
            new_user_name = input('new name: ')
            dbm.rename_user(uname, new_user_name)
            uname = new_user_name
        elif cmd in ['D', 'd']:
            sure = input(
                'To confirm, type the user name you want to delete: ',
            )
            if sure == uname:
                user_id = dbm.get_user_id_by_name(uname)
                dbm.delete_games_by_userid(user_id)
                dbm.delete_user(uname)
                break
        elif cmd in ['L', 'l']:
            print('Summary:')
            won, lost = dbm.get_game_stats_by_user(uname)
            print(f'Won: {won}, Lost: {lost}')
            print('-' * 20)
            print('Games:')
            for ugc, ggc, won in dbm.get_game_details_by_user(uname):
                print(f'user guessed: {ugc}, game guessed: {ggc}, {won}')


def main() -> int:
    dbm = DBManager()
    while True:
        cmd = input('> ')
        if cmd in ['Q', 'q']:
            break
        elif cmd == 'h':
            print(
                '''\
            u - user menu
            w - word menu
            q - quit
            ''',
            )
        elif cmd == 'u':
            user_menu(dbm)
        elif cmd == 'w':
            word_menu(dbm)
        else:
            pass
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
