import argparse

from libs.cli import Cli

debug = False

# TODO: chose from multiple word DBs - maybe one per language?


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

    cli = Cli(args.l, args.chars)
    return cli.run()


if __name__ == '__main__':
    raise SystemExit(main())
