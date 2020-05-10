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

PASSWORD_HASHES = [
    'pbkdf2_sha256$180000$KCxbsQtjlf5c$GWmFNc2X0IfEstU4ncok+9WEGq3Jj7oHypdyf/2z+1k=',
    'pbkdf2_sha256$180000$tCcmwmGq8DS4$dfH+rVOqkQSeLJDcNpZmkWPSyYQhKdC/UvaH6yt8Oh8=',
    'pbkdf2_sha256$180000$YGOegNNQbuTv$xthOdv3ebGz0t/yJBF1qfFeIx0Q5AGx1VCAl31O9H80=',
    'pbkdf2_sha256$180000$gmhPffvNL6ky$0ElRlCDw27D0A7MR20JzA6WZrSriN/9fBqaZugg9M5k=',
    'pbkdf2_sha256$180000$pQXNuVNqjcgS$Oj4X+LKR+EoRJVyQlIj9p3vitIOOvNayK9ZDo0eip1Y=',
]

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
