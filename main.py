from game import SpyGame

def main():
    n = 1_964_556_481
    e = 456_899

    game = SpyGame(n=n, e=e)
    game.run()


if __name__ == "__main__":
    main()