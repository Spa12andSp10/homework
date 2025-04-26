from sqlite3 import connect

connection = connect("base.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Goods`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `genre_id` INTEGER NOT NULL,
    `name` TEXT NOT NULL,
    `prise` INTEGER NOT NULL,
    `quantity` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Genres`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `name` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Clients`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `name` TEXT NOT NULL,
    `surname` TEXT NOT NULL,
    `phone_number` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Receipts`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `date` TEXT NOT NULL,
    `total_amount` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Receipt_items`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `receipts_id` INTEGER NOT NULL,
    `client_id` INTEGER NOT NULL,
    `product_id` INTEGER NOT NULL,
    `quantity` INTEGER NOT NULL,
    `total` INTEGER NOT NULL
);
""")

for s in open("w1.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Goods`
    (`id`,`genre_id`, `name`, `prise`, `quantity`) VALUES(?,?,?,?,?)""",
                   (int(data[0]), int(data[1]), data[2], int(data[3]), int(data[4])))

for s in open("w2.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Genres`(`id`,`name`) 
    VALUES(?,?)""",
                   (int(data[0]), data[1]))

for s in open("w3.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Clients`(`id`,`name`,`surname`,`phone_number`) VALUES(?,?,?,?)""",
                   (int(data[0]), data[1], data[2], data[3]))


for s in open("w5.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Receipts`
    (`id`,`date`, `total_amount`) 
    VALUES(?,?,?)""",
                   (int(data[0]), data[1], int(data[2])))

for s in open("w4.txt", encoding='utf-8'):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Receipt_items`
    (`id`,`receipts_id`, `client_id`, `product_id`, `quantity`, `total`) VALUES(?,?,?,?,?,?)""",
                   (int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5])))

connection.commit()
connection.close()

