from sqlite3 import connect

connection = connect("base.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Movements`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `date` TEXT NOT NULL,
    `id_shop` TEXT NOT NULL,
    `id_product` INTEGER NOT NULL,
    `number_of_packages` INTEGER NOT NULL,
    `type_of_operation` TEXT NOT NULL,
    `cost` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Goods`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `department` TEXT NOT NULL,
    `product` TEXT NOT NULL,
    `unit_of_measurement` TEXT NOT NULL,
    `quantity` TEXT NOT NULL,
    `provider` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Shops`(
    `id` TEXT PRIMARY KEY NOT NULL UNIQUE,
    `district` TEXT NOT NULL,
    `address` TEXT NOT NULL
);
""")

for s in open("work1.txt"):
    data = s.split()
    cursor.execute("""INSERT OR REPLACE INTO `Movements`
    (`id`,`date`,`id_shop`,`id_product`,`number_of_packages`,`type_of_operation`,`cost`) VALUES(?,?,?,?,?,?,?)""",
                   (int(data[0]), data[1], data[2], int(data[3]), int(data[4]), data[5], int(data[6])))

for s in open("work2.txt"):
    data = s.split()
    cursor.execute("""INSERT OR REPLACE INTO `Goods`(`id`,`department`,`product`,`unit_of_measurement`,`quantity`,`provider`) 
    VALUES(?,?,?,?,?,?)""",
                   (int(data[0]), data[1], data[2], data[3], data[4], data[5]))

for s in open("work3.txt"):
    data = s.split()
    cursor.execute("""INSERT OR REPLACE INTO `Shops`(`id`,`district`,`address`) VALUES(?,?,?)""",
                   (data[0], data[1], data[2]))


connection.commit()

cursor.execute("""
    SELECT 
        m.id AS movement_id,
        m.number_of_packages,
        m.type_of_operation,
        s.district AS shop_district,
        g.product
    FROM Movements m
    JOIN Shops s ON m.id_shop = s.id
    JOIN Goods g ON m.id_product = g.id
    WHERE s.district = 'Заречный' AND g.product = 'Яйцо_диетическое' AND m.type_of_operation = "Поступление"
""")



d = cursor.fetchall()

post = 0

if d:
    for row in d:
        post += row[1]

cursor.execute("""
    SELECT 
        m.id AS movement_id,
        m.number_of_packages,
        m.type_of_operation,
        s.district AS shop_district,
        g.product
    FROM Movements m
    JOIN Shops s ON m.id_shop = s.id
    JOIN Goods g ON m.id_product = g.id
    WHERE s.district = 'Заречный' AND g.product = 'Яйцо_диетическое' AND m.type_of_operation = "Продажа"
""")

d2 = cursor.fetchall()

pro = 0

if d2:
    for row in d2:
        pro += row[1]

print(post - pro)
connection.close()

