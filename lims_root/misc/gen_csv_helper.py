from random import randint

ACCOUNT_NAME_FILE = 'names/names.txt'
APPARATUS_NAME_FILE = 'hardware.txt'

ROLES_IDS = {
    'ADM': [i for i in range(2, 4)],
    'STA': [i for i in range(4, 10)],
    'TEA': [i for i in range(10, 50)],
    'STU': [i for i in range(50, 150)],
    'VIS': [i for i in range(150, 180)],
}

CAMPUS_IDS = set([
    str(randint(2000, 2020)) + str(randint(1000, 9999))
    for i in range(500)
])

SCHOOL_CHOICES = (
    ('CS', 'Computer Science'),
    ('CE', 'Communication Engineering'),
    ('OE', 'OptoElectronic Engineering'),
    ('SE', 'Big Data and Software Engineering'),
    ('AUTO', 'Automation'),
)

EMAIL_SUFFIX = (
    '@gmail.com',
    '@outlook.com',
    '@random.org',
    '@cqu.edu.cn',
    '@somesite.net',
)

PASSWORD_HASHES = (
    'pbkdf2_sha256$180000$NgmVkPjQVft1$gjw0B44I/q1HrvHpWGg0kmH8XswGWtsvW8ZwlaKEIdg=',
)

LABORATORY_NAMES = (
    'VR Experience', 'Computer Vision', 'IoT', '5G/6G Research',
    'Limit Computing', 'Cloud Computing', 'Machine Learning',
    'Data Mining Center', 'Training Plaza', 'Linux Center',
    'Teaching Plaza', 'Multi-Functional Room', 'Multimedia',
)


def load_account_names():
    infile = open(ACCOUNT_NAME_FILE, "r")
    names = set([line.strip().title() for line in infile.readlines()])
    infile.close()
    return names


def load_apparatus_names():
    infile = open(APPARATUS_NAME_FILE, "r")
    names = set([line.strip().upper() for line in infile.readlines()])
    infile.close()
    return names


def get_email_by_account_name(name):
    pieces = name.split(" ")
    return (pieces[0][0] + pieces[len(pieces) - 1] +
            EMAIL_SUFFIX[randint(0, len(EMAIL_SUFFIX) - 1)]).lower()
