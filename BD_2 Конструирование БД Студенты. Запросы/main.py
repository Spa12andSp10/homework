from sqlite3 import connect

connection = connect("base.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Students`(
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `level_id` INTEGER NOT NULL,
    `direction_id` INTEGER NOT NULL,
    `type_of_training_id` INTEGER NOT NULL,
    `surname` TEXT NOT NULL,
    `name` TEXT NOT NULL,
    `patronymic` TEXT NOT NULL,
    `average_score` INTEGER NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Levels`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `title` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Directions`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `title` TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `Types`(
    `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    `title` TEXT NOT NULL
);
""")

for s in open("w1.txt"):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Levels`
    (`id`,`title`) VALUES(?,?)""",
                   (int(data[0]), data[1]))

for s in open("w2.txt"):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Directions`(`id`,`title`) 
    VALUES(?,?)""",
                   (int(data[0]), data[1]))

for s in open("w3.txt"):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Types`(`id`,`title`) VALUES(?,?)""",
                   (data[0], data[1]))


for s in open("w4.txt"):
    data = s.split()
    cursor.execute("""INSERT OR IGNORE INTO `Students`
    (`id`,`level_id`, `direction_id`, `type_of_training_id`, `surname`, `name`, `patronymic`, `average_score`) 
    VALUES(?,?,?,?,?,?,?,?)""",
                   (int(data[0]), int(data[1]), int(data[2]), int(data[3]), data[4], data[5], data[6], int(data[7])))

connection.commit()

cursor.execute("""
    SELECT COUNT(id)
    FROM Students
""")

cnt = cursor.fetchone()

print(f"Количество всех студентов равно {cnt[0]}")

cursor.execute("""
    SELECT d.title, COUNT(s.id)
    FROM Students s
    JOIN Directions d ON s.direction_id = d.id
    GROUP BY d.title
""")

res = cursor.fetchall()

print("\nСтуденты по направлениям")
for r in res:
    print(f"Направление: {r[0]} - {r[1]}")

cursor.execute("""
    SELECT t.title, COUNT(s.id)
    FROM Students s
    JOIN Types t ON s.type_of_training_id = t.id
    GROUP BY t.title
""")

res = cursor.fetchall()

print("\nСтуденты по формам обучения")
for r in res:
    print(f"Форма: {r[0]} - {r[1]}")

cursor.execute("""
    SELECT d.title, MAX(s.average_score), MIN(s.average_score), AVG(s.average_score)
    FROM Students s
    JOIN Directions d ON s.direction_id = d.id
    GROUP BY d.title
""")

res = cursor.fetchall()

print("\nМаксимальный, минимальный и средний баллы по направлениям")
for r in res:
    print(f"Направление: {r[0]}, максимальный балл: {r[1]}, минимальный балл: {r[2]}, средний балл: {r[3]}")

cursor.execute("""
    SELECT t.title, AVG(s.average_score)
    FROM Students s
    JOIN Types t ON s.type_of_training_id = t.id
    GROUP BY t.title
""")

res = cursor.fetchall()

print("\nСредний балл по формам обучения")
for r in res:
    print(f"Форма обучения: {r[0]} - {r[1]}")

cursor.execute("""
    SELECT l.title, AVG(s.average_score)
    FROM Students s
    JOIN Levels l ON s.level_id = l.id
    GROUP BY l.title
""")

res = cursor.fetchall()

print("\nСредний балл по уровням обучения")
for r in res:
    print(f"Уровень обучения: {r[0]} - {r[1]}")

cursor.execute("""
    SELECT t.title, s.surname, d.title, s.average_score 
    FROM Students s
    JOIN Types t ON s.type_of_training_id = t.id
    JOIN Directions d ON s.direction_id = d.id
    WHERE d.title = 'Разработка' OR d.title = 'Дизайн' AND t.title = 'Очное'
    GROUP BY s.surname
    ORDER BY s.average_score
""")

res = cursor.fetchall()

print("\nТоп 5 (вернее топ 3 так как мало людей соответвующих условию) для повышенной стипендии")
for r in res:
    print(f"Балл: {r[3]}, фамилия: {r[1]}")

cursor.execute("""
    SELECT surname, count(*)
    FROM Students
    GROUP BY surname
    HAVING count(*) > 1
""")

res = cursor.fetchall()

print("\nКоличество отдофамильцев")
for r in res:
    print(f"Фамилия: {r[0]} - {r[1]}")

cursor.execute("""
    SELECT surname, name, patronymic, count(*)
    FROM Students
    GROUP BY surname, name, patronymic
    HAVING count(*) > 1
""")

res = cursor.fetchall()

print("\nЧисло людей, которые полные тезки")
for r in res:
    print(f"{r[0]} {r[1]} {r[2]} - {r[3]}")

connection.close()