from random import randint

from misc.randchar import \
    random_cost, random_date, random_datetime, \
    random_location, random_model_no, random_time

IN_FILE = 'hardware.txt'
OUT_FILE = 'db.py'
TABLES = ('inventory_facility', 'inventory_apparatus',
          'inventory_laboratory', 'bulletin_article',
          'bulletin_facilityschedule',)
STAFF_IDS = (2, 3,)
LAB_NAMES = ('AI', 'VR', 'AR', 'Computer Vision',
             'Advanced DIP', 'IoT', '5G/6G', 'Margin Computing',
             'Cloud Computing', 'Post Quantum Cryptography',
             'Machine Learning', 'Data Mining Center', 'Training Plaza',
             'Linux Center', 'Teaching Plaza', 'Multi-Functional Room',
             'Multimedia',)
SCHOOL_CHOICES = (
    ('CS', 'Computer Science'),
    ('CE', 'Communication Engineering'),
    ('OE', 'OptoElectronic Engineering'),
    ('SE', 'Big Data and Software Engineering'),
    ('AUTO', 'Automation'),
)

infile = open(IN_FILE, "r")
outfile = open(OUT_FILE, "w")
facility_id = 1


def prepare():
    outfile.write("import sqlite3\n\n"
                  "db = sqlite3.connect(\"../db.sqlite3\")\n"
                  "cursor = db.cursor()\n\n\n")


def finish():
    outfile.write("db.commit()\n")
    outfile.write("db.close()\n")


def delete():
    for table in TABLES:
        outfile.write("cursor.execute(\""
                      "delete from " + table + ";\")\n")

    outfile.write("\n\n")


def gen_facility(fid, staff_id, school, name):
    outfile.write("cursor.execute(\""
                  "insert into inventory_facility "
                  "(id, staff_id, school, name) values ("
                  + str(fid) + ", " + str(staff_id) + ", '"
                  + str(school) + "', '" + str(name) + "');\")\n")


def gen_apparatus(fid, model_no, cost, purchased):
    outfile.write("cursor.execute(\""
                  "insert into inventory_apparatus "
                  "(facility_ptr_id, model_no, cost, purchased) values ("
                  + str(fid) + ", '" + str(model_no) + "', "
                  + str(cost) + ", '" + str(purchased) + "');\")\n")


def gen_apparatuses(repeat_chance=20):
    global facility_id
    apparatus_ids = set()

    for line in infile.readlines():
        facility_name = line.strip().upper()

        while True:
            gen_facility(facility_id,
                         STAFF_IDS[randint(0, len(STAFF_IDS) - 1)],
                         SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
                         facility_name)
            apparatus_ids.add(facility_id)
            facility_id += 1
            if randint(1, 100) > repeat_chance:
                break

    outfile.write("\n\n")

    for apparatus_id in apparatus_ids:
        gen_apparatus(apparatus_id, random_model_no(),
                      random_cost(), random_date())

    outfile.write("\n\n")


def gen_lab(fid, location, capacity):
    outfile.write("cursor.execute(\""
                  "insert into inventory_laboratory "
                  "(facility_ptr_id, location, capacity) values ("
                  + str(fid) + ", '" + str(location) + "', "
                  + str(capacity) + ");\")\n")


def gen_labs(nlab=60):
    global facility_id
    lab_ids = set()

    for i in range(nlab):
        gen_facility(facility_id,
                     STAFF_IDS[randint(0, len(STAFF_IDS) - 1)],
                     SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
                     LAB_NAMES[randint(0, len(LAB_NAMES) - 1)])
        lab_ids.add(facility_id)
        facility_id += 1

    outfile.write("\n\n")

    for lab_id in lab_ids:
        gen_lab(lab_id, random_location(), randint(3, 30))

    outfile.write("\n\n")


def gen_article(aid, published, subject, content):
    outfile.write("cursor.execute(\""
                  "insert into bulletin_article "
                  "(id, published, subject, content) values ("
                  + str(aid) + ", '" + str(published) + "', '"
                  + str(subject) + "', '" + str(content)
                  + "');\")\n")


def gen_articles(narticle=25):
    for i in range(1, narticle + 1):
        gen_article(i, random_datetime(2010, 2020),
                    "Here is the subject for news #" + str(i),
                    "Here is the corresponding content for news #" + str(i) +
                    "  " +
                    "Roses are red, " +
                    "violets are blue. " +
                    "A face like yours, " +
                    "belongs to the zoo. ")
    outfile.write("\n\n")


def gen_schedule(sid, school, site, day, start, end):
    outfile.write("cursor.execute(\""
                  "insert into bulletin_facilityschedule "
                  "(id, school, site, day, start, end) values ("
                  + str(sid) + ", '" + str(school) + "', '"
                  + str(site) + "', '" + str(day) + "', '"
                  + str(start) + "', '" + str(end)
                  + "');\")\n")


def gen_schedules(nschedule=50):
    for i in range(1, nschedule + 1):
        gen_schedule(i,
                     SCHOOL_CHOICES[randint(0, len(SCHOOL_CHOICES) - 1)][0],
                     random_location(),
                     random_date(2020, 2021),
                     random_time(8, 12),
                     random_time(14, 18))
    outfile.write("\n\n")


def main():
    prepare()
    delete()

    gen_apparatuses()
    gen_labs()
    gen_articles()
    gen_schedules()

    finish()


main()
infile.close()
outfile.close()
