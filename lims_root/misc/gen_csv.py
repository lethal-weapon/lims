from misc.gen_csv_helper import *
from misc.random_src import random_cost, random_date, random_location, random_model_no

OUT_FILES = [
    'csv/accounts.csv',
    'csv/apparatuses.csv',
    'csv/laboratories.csv',
]

MODEL_FIELDS = [
    'id,password,email,campus_id,name,school,limit,role,is_active,is_verified',
    'id,name,staff,school,cost,model_no,purchased',
    'id,name,staff,school,location,capacity',
]

FACILITY_ID = 1


def gen_accounts():
    ACCOUNT_NAMES = load_account_names()
    accounts = []

    for role, ids in ROLES_IDS.items():
        for account_id in ids:
            name = ACCOUNT_NAMES.pop()
            accounts.append({
                'id'         : account_id,
                'password'   : PASSWORD_HASHES[randint(0, len(PASSWORD_HASHES) - 1)],
                'email'      : get_email_by_account_name(name),
                'campus_id'  : CAMPUS_IDS.pop(),
                'name'       : name,
                'school'     : SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
                'limit'      : randint(0, 5),
                'role'       : role,
                'is_active'  : True,
                'is_verified': False if role == 'VIS' else True,
            })

    return accounts


def gen_apparatuses(repeat_chance=25):
    global FACILITY_ID
    apparatuses = []
    APPARATUS_NAMES = load_apparatus_names()

    while len(APPARATUS_NAMES) > 0:
        name = APPARATUS_NAMES.pop()

        while True:
            apparatuses.append({
                'id'       : FACILITY_ID,
                'name'     : name,
                'staff'    : ROLES_IDS['STA'][randint(0, len(ROLES_IDS['STA']) - 1)],
                'school'   : SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
                'cost'     : random_cost(),
                'model_no' : random_model_no(),
                'purchased': random_date(),
            })
            FACILITY_ID += 1
            if randint(1, 100) > repeat_chance:
                break

    return apparatuses


def gen_labs(rooms=75):
    global FACILITY_ID
    laboratories = []

    for i in range(rooms):
        laboratories.append({
            'id'      : FACILITY_ID,
            'name'    : LABORATORY_NAMES[randint(0, len(LABORATORY_NAMES) - 1)],
            'staff'   : ROLES_IDS['STA'][randint(0, len(ROLES_IDS['STA']) - 1)],
            'school'  : SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
            'location': random_location(),
            'capacity': randint(3, 33),
        })
        FACILITY_ID += 1

    return laboratories


def main():
    mappings = {
        0: gen_accounts,
        1: gen_apparatuses,
        2: gen_labs,
    }

    for index, generator in mappings.items():
        field_names = MODEL_FIELDS[index].split(',')
        instances = generator()

        outfile = open(OUT_FILES[index], "w")
        outfile.write(MODEL_FIELDS[index] + "\n")

        for instance in instances:
            outfile.write(",".join([
                str(instance[name]) for name in field_names
            ]))
            outfile.write("\n")

        outfile.close()


main()
