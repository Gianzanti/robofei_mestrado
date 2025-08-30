import sys

from robofei import greet


def main():
    if len(sys.argv) > 1:
        print(greet(sys.argv[1]))
    else:
        print(greet("world"))

if __name__ == "__main__":
    main()

