from datetime import datetime
from random import randint


# Generate a random character between ch1 and ch2
def getRandomCharacter(ch1, ch2):
    return chr(randint(ord(ch1), ord(ch2)))


# Generate a random lowercase letter
def getRandomLowerCaseLetter():
    return getRandomCharacter('a', 'z')


# Generate a random uppercase letter
def getRandomUpperCaseLetter():
    return getRandomCharacter('A', 'Z')


# Generate a random digit character
def getRandomDigitCharacter(length=1):
    string = ""
    for i in range(length):
        string += getRandomCharacter('0', '9')
    return string


def getRandomPositiveDigit():
    return getRandomCharacter('1', '9')


# Generate a random character
def getRandomASCIICharacter():
    return getRandomCharacter(chr(0), chr(127))


# Generate a random letter string
def getRandomLetterString(length):
    string = ""
    for i in range(length):
        if randint(0, 1) == 0:
            string += getRandomUpperCaseLetter()
        else:
            string += getRandomLowerCaseLetter()
    return string


# Generate a random ascii string
def getRandomASCIIString(length):
    string = ""
    for i in range(length):
        string += getRandomASCIICharacter()
    return string


def random_model_no():
    string = ""
    length = randint(4, 9)

    for i in range(length):
        if randint(0, 1) == 0:
            string += getRandomUpperCaseLetter()
        else:
            string += getRandomDigitCharacter()
    return string


def random_location():
    LETTERS = ('C', 'B', 'A', 'DZ', 'DS',)
    string = ""
    rand = randint(0, 9)

    if rand >= 9:
        string += LETTERS[0]
    elif rand >= 7:
        string += LETTERS[1]
    elif rand >= 5:
        string += LETTERS[2]
    elif rand >= 4:
        string += LETTERS[3]
    else:
        string += LETTERS[4]

    for i in range(4):
        string += getRandomPositiveDigit()

    return string


def random_cost(MIN=9, MAX=999):
    return str(randint(MIN, MAX) + (randint(0, 9) * 10 / 100)) + "0"


def random_date(year_start=2000, year_end=2020):
    return datetime.today().date().replace(
        year=randint(year_start, year_end),
        month=randint(1, 12),
        day=randint(1, 28))


def random_time(hour_start=0, hour_end=23):
    return datetime.today().time().replace(
        hour=randint(hour_start, hour_end),
        minute=randint(0, 59),
        second=randint(0, 59))


def random_datetime(year_start=2000, year_end=2020,
                    hour_start=0, hour_end=23):
    return datetime.today().replace(
        year=randint(year_start, year_end),
        month=randint(1, 12),
        day=randint(1, 28),
        hour=randint(hour_start, hour_end),
        minute=randint(0, 59),
        second=randint(0, 59))
