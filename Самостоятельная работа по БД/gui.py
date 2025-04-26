import tkinter as tk
from tkinter import messagebox
from sqlite3 import connect

conn = connect("base.db")
cursor = conn.cursor()

root = tk.Tk()
root.title("Анализ продаж магазина")
root.geometry("600x600")

def show_total():
    cursor.execute("SELECT SUM(total_amount) FROM Receipts")
    res = cursor.fetchone()[0]
    result_label.config(text=f"Общая сумма всех продаж: {res} руб.")


def show_date_sales():
    date = date_entry.get()

    try:
        year, month, day = date.split("-")
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise ValueError
        int(year), int(month), int(day)
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД (например: 2023-05-15)")
        return

    cursor.execute("SELECT SUM(total_amount) FROM Receipts WHERE date = ?", (date,))
    result = cursor.fetchone()[0] or 0
    if result:
        result_label.config(text=f"Продажи за {date}: {result} руб.")
    else:
        result_label.config(text=f"Дата не найдена")

def show_game_sales():
    date = date_game_entry.get()

    try:
        year, month, day = date.split("-")
        if len(year) != 4 or len(month) != 2 or len(day) != 2:
            raise ValueError
        int(year), int(month), int(day)
    except ValueError:
        messagebox.showwarning("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД (например: 2023-05-15)")
        return

    cursor.execute("""
        SELECT ri.quantity, r.date, g.name
        FROM Receipt_items ri
        JOIN Goods g ON ri.product_id = g.id
        JOIN Receipts r ON ri.receipts_id = r.id
        WHERE r.date = ?
    """, (date, ))
    results = cursor.fetchall()
    if results:
        text = "Продажи игр за дату:\n"
        for result in results:
            r = " ".join(result[2].split("_"))
            text += f"Игра: {r}, количество продаж: {result[0]}\n"
        result_label.config(text=text)
    else:
        result_label.config(text="Нет продаж за указанную дату")


def show_clients_sales():
    surname = surname_entry.get()
    name = name_entry.get()

    if not surname or not name:
        messagebox.showwarning("Ошибка", "Введите фамилию и имя клиента")
        return

    cursor.execute("""
        SELECT SUM(ri.total) 
        FROM Receipt_items ri
        JOIN Clients c ON ri.client_id = c.id
        WHERE c.surname = ? AND c.name = ?
    """, (surname, name))

    total = cursor.fetchone()[0]
    if total:
        result_label.config(text=f"Клиент {surname} {name} потратил {total} рублей")
    else:
        result_label.config(text=f"Клиент не найден")

tk.Button(root, text="Общая прибыль", command=show_total).pack(pady=5)

date_frame = tk.Frame(root)
date_frame.pack(pady=5)
tk.Label(date_frame, text="Дата (ГГГГ-ММ-ДД):").pack(side=tk.LEFT)
date_entry = tk.Entry(date_frame, width=15)
date_entry.pack(side=tk.LEFT, padx=5)
tk.Button(date_frame, text="Показать продажи за дату",command=show_date_sales).pack(side=tk.LEFT)

date_and_game_frame = tk.Frame(root)
date_and_game_frame.pack(pady=5)
tk.Label(date_and_game_frame, text="Дата (ГГГГ-ММ-ДД):").pack(side=tk.LEFT)
date_game_entry = tk.Entry(date_and_game_frame, width=15)
date_game_entry.pack(side=tk.LEFT, padx=5)
tk.Button(date_and_game_frame, text="Показать игры проданные в эту дату",command=show_game_sales).pack(side=tk.LEFT)

name_frame = tk.Frame(root)
name_frame.pack(pady=5)
tk.Label(name_frame, text="Фамилия").pack(side=tk.LEFT)
surname_entry = tk.Entry(name_frame, width=15)
surname_entry.pack(side=tk.LEFT, padx=5)
tk.Label(name_frame, text="Имя").pack(side=tk.LEFT)
name_entry = tk.Entry(name_frame, width=15)
name_entry.pack(side=tk.LEFT, padx=5)
tk.Button(name_frame, text="Показать сколько потратил клиент",command=show_clients_sales).pack(side=tk.LEFT)

result_label = tk.Label(root, text="", font=('Arial', 14), fg='black')
result_label.pack(pady=20)
def on_closing():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
