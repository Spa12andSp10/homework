from sqlite3 import connect

connection = connect("base_db")
cur = connection.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS `Employees` (
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `name` TEXT NOT NULL,
    `lastname` TEXT NOT NULL,
    `phone_number` TEXT NOT NULL,
    `post_id` INTEGER NOT NULL,
    FOREIGN KEY(`post_id`) REFERENCES `Employee_positions`(`id`)
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS `Employee_positions` (
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `name` TEXT NOT NULL
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS `Customers` (
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `organization` TEXT NOT NULL,
    `phone_number` TEXT NOT NULL
);
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS `Orders` (
    `id` INTEGER PRIMARY KEY NOT NULL UNIQUE,
    `customer_id` INTEGER NOT NULL,
    `employee_id` INTEGER NOT NULL,
    `amount` INTEGER NOT NULL,
    `date_of_completion` TEXT NOT NULL,
    `mark_of_completion` TEXT NOT NULL,
    FOREIGN KEY(`customer_id`) REFERENCES `Customers`(`id`),
    FOREIGN KEY(`employee_id`) REFERENCES `Employees`(`id`)
);
""")

positions = [
    (1, "Manager"),
    (2, "Developer"),
    (3, "Designer"),
    (4, "Analyst"),
    (5, "Director")
]
cur.executemany("INSERT OR IGNORE INTO `Employee_positions`(`id`, `name`) VALUES(?, ?)", positions)

employees_data = [
    (1, "Ivan", "Ivanov", "+7(912)345-67-89", 2),
    (2, "Petr", "Petrov", "+7(987)654-32-10", 1),
    (3, "Maria", "Sidorova", "+7(926)123-45-67", 3),
    (4, "Aleksey", "Alekseev", "+7(905)678-90-12", 2),
    (5, "Ekaterina", "Smirnova", "+7(999)888-77-66", 3),
    (6, "Dmitry", "Kuznetsov", "+7(916)555-44-33", 4),
    (7, "Anna", "Petrova", "+7(903)222-11-00", 1),
    (8, "Igor", "Volkov", "+7(925)777-66-55", 5),
    (9, "Olga", "Morozova", "+7(901)234-56-78", 4),
    (10, "Sergey", "Pleskunov", "+7(913)987-65-43", 2)
]

cur.executemany("""
    INSERT OR IGNORE INTO `Employees`(`id`, `name`, `lastname`, `phone_number`, `post_id`)
    VALUES(?, ?, ?, ?, ?)
""", employees_data)

сustomers_data = [
    (1, "TechnoProfi", "+7(915)123-45-67"),
    (2, "StartUp Logistics", "+7(926)987-65-43"),
    (3, "GlobalService", "+7(903)456-78-90"),
    (4, "Innovative Solutions", "+7(999)111-22-33"),
    (5, "EcoTrade", "+7(916)777-88-99")
]

cur.executemany("""
    INSERT OR IGNORE INTO `Customers`(`id`,`organization`,`phone_number`) VALUES(?,?,?)
""", сustomers_data)

orders_data = [
    (1, 1, 10, 90000, "20.11.2024", "completed"),
    (2, 1, 9, 85000, "22.11.2024", "not completed"),
    (3, 5, 6, 90000, "03.01.2025", "completed"),
    (4, 3, 2, 95000, "01.02.2025", "completed"),
    (5, 2, 7, 65000, "04.03.2025", "not completed"),
    (6, 2, 8, 110000, "15.02.2024", "completed"),
    (7, 4, 5, 84000, "25.07.2023", "completed"),
    (8, 4, 10, 115000, "19.06.2024", "completed"),
    (9, 5, 1, 86000, "18.03.2025", "not completed"),
    (10, 2, 4, 100000, "12.12.2024", "not completed")
]

cur.executemany("""
    INSERT OR IGNORE INTO `Orders`(`id`,`customer_id`,`employee_id`,`amount`,`date_of_completion`,`mark_of_completion`)
    VALUES(?,?,?,?,?,?)
""", orders_data)

connection.commit()

cur.execute("""
    SELECT o.amount, e.lastname,
    CASE
        WHEN o.amount < 85000 THEN 'Малая выплата'
        WHEN o.amount BETWEEN 85000 AND 100000 THEN 'Средняя выплата'
        ELSE 'Высокая выплата'
    END AS payout_amount
    FROM Employees e
    JOIN Orders o ON o.employee_id = e.id  
""")

res = cur.fetchall()

for i in res:
    print(f"Фамилия: {i[1]}, Размер выплаты: {i[0]} - {i[2]}")


cur.execute("""
    SELECT ep.name, e.lastname,
    CASE
        WHEN ep.name = 'Developer' OR ep.name = 'Designer' THEN 'Первый отдел'
        WHEN ep.name = 'Analyst' OR ep.name = 'Manager' THEN 'Второй отдел'
        ELSE 'Нулевой отдел'
    END AS department
    FROM Employees e
    JOIN Employee_positions ep ON e.post_id = ep.id  
""")

res = cur.fetchall()

print("\nСотрудники по отделам")
for i in res:
    print(f"Фамилия: {i[1]}, Профессия: {i[0]} - {i[2]}")


cur.execute("""
    SELECT *
    FROM Orders
    WHERE amount > (SELECT AVG(amount) FROM Orders) AND mark_of_completion = 'completed';
""")

res = cur.fetchall()

print("\nВыплата больше средней")
for i in res:
    print(i[3])

cur.execute("""
    SELECT o.amount, c.organization
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.id
    WHERE o.amount <= (SELECT AVG(amount) FROM Orders)
    ORDER BY c.organization
""")

res = cur.fetchall()

print("\nОрганизации, которые заплатили выплату, которая меньше или равна средней")
for i in res:
    print(f"Организация {i[1]} - {i[0]}")

cur.execute("""
    WITH position AS(
    SELECT e.lastname, ep.name
    FROM Employees e
    JOIN Employee_positions ep ON e.post_id = ep.id
    WHERE ep.name = 'Analyst'
    )
    SELECT *
    FROM position;
""")

res = cur.fetchall()

print("\nАналитики")
for i in res:
    print(f"Фамилия {i[0]} - {i[1]}")

cur.execute("""
    WITH not_completed AS(
    SELECT e.lastname, o.mark_of_completion
    FROM Orders o
    JOIN Employees e ON o.employee_id = e.id
    WHERE o.mark_of_completion = 'not completed'
    )
    SELECT *
    FROM not_completed;
""")

res = cur.fetchall()

print("\nЛюди, которые не выполнили работу")
for i in res:
    print(f"Фамилия {i[0]} - {i[1]}")

connection.close()