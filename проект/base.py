from sqlite3 import connect
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

connection = connect("base.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Specializations` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Reception_hours` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `time` FLOAT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Hours` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `start_hour` INTEGER NOT NULL,
    `finish_hour` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Offices` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `office` INTEGER NOT NULL
);
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Patients` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `name` TEXT NOT NULL,
    `surname` TEXT NOT NULL,
    `patronymic` TEXT NOT NULL,
    `polis` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Doctors` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `specialization_id` INTEGER NOT NULL,
    `office_id` INTEGER NOT NULL,
    `time_id` INTEGER NOT NULL,
    `name` TEXT NOT NULL,
    `surname` TEXT NOT NULL,
    `patronymic` TEXT NOT NULL,
    `special_number` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Medical_receptions` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `doctor_id` INTEGER NOT NULL,
    `patient_id` INTEGER NOT NULL,
    `time_id` INTEGER NOT NULL
);
""")

for s in open("table1.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Specializations`
    (`name`) VALUES(?)""",
                   (data))

for s in open("table2.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Reception_hours`(`time`) 
    VALUES(?)""",
                   (data))

for s in open("table3.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Hours`(`start_hour`,`finish_hour`) VALUES(?,?)""",
                   (int(data[0]), int(data[1])))


for s in open("table4.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Offices`
    (`office`) 
    VALUES(?)""",
                   (data))


for s in open("table7.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Doctors`
    (`specialization_id`, `office_id`, `time_id`, `name`, `surname`, `patronymic`, `special_number`) VALUES(?,?,?,?,?,?,?)""",
                   (int(data[0]), int(data[1]), int(data[2]), data[3], data[4], data[5], int(data[6])))

for s in open("table6.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Patients`
    (`name`, `surname`, `patronymic`, `polis`) VALUES(?,?,?,?)""",
                   (data[0], data[1], data[2], data[3]))

for s in open("table8.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Medical_receptions`
    (`doctor_id`, `patient_id`, `time_id`) VALUES(?,?,?)""",
                   (int(data[0]), int(data[1]), int(data[2])))

connection.commit()



connection.close()