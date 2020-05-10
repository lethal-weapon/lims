from random import randint

from misc.random_src import getRandomUpperCaseLetter

OUT_FILE = 'names.txt'
IN_FILES = [
    'female-first.txt',
    'male-first.txt',
    'last-name.txt',
]


def read_names(index):
    infile = open(IN_FILES[index], "r")
    names = set()

    for line in infile.readlines():
        names.add(line.strip().upper())

    infile.close()
    return names


def main():
    last_names = read_names(2)
    first_names = read_names(0).union(read_names(1))

    outfile = open(OUT_FILE, "w")
    while len(last_names) > 0:

        # 10% chance the name contains middle initial
        if randint(0, 9) == 0:
            outfile.write(first_names.pop()
                          + " " + getRandomUpperCaseLetter() + ". "
                          + last_names.pop() + "\n")
        else:
            outfile.write(first_names.pop() + " " + last_names.pop() + "\n")

    outfile.close()


main()
