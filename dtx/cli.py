import argparse

def main():
    parser = argparse.ArgumentParser(
        prog="dtx",
        description="Minimalist dotfiles manager"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    init_parser = subparsers.add_parser("init", help="Initialize the dotfiles directory")

    args = parser.parse_args()

    if args.command == "init":
        print("Coming Soon . . .")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()