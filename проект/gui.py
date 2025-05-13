import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sqlite3 import connect
import hashlib

conn = connect("base.db")
cursor = conn.cursor()

root = tk.Tk()
root.title("Регистрация")
root.geometry("500x350")
root.configure(bg='lightblue')

root.surname_entry = None
root.name_entry = None
root.patronymic_entry = None
root.polis_entry = None
root.specialization_frame = None
root.doctor_combo = None
root.time_combo = None

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
def open_registration():
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Регистрация")
    new_window.geometry("300x500")

    tk.Label(new_window,
             text="Регистрация",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)

    surname_frame = tk.Frame(new_window, background='lightblue')
    surname_frame.pack(pady=5)
    tk.Label(surname_frame, text="Фамилия", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.surname_entry = tk.Entry(surname_frame, width=15, font=("Arial", 12))
    root.surname_entry.pack(side=tk.LEFT, padx=5)

    name_frame = tk.Frame(new_window, background='lightblue')
    name_frame.pack(pady=5)
    tk.Label(name_frame, text="Имя", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.name_entry = tk.Entry(name_frame, width=15, font=("Arial", 12))
    root.name_entry.pack(side=tk.LEFT, padx=5)

    patronymic_frame = tk.Frame(new_window, background='lightblue')
    patronymic_frame.pack(pady=5)
    tk.Label(patronymic_frame, text="Отчество", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.patronymic_entry = tk.Entry(patronymic_frame, width=15, font=("Arial", 12))
    root.patronymic_entry.pack(side=tk.LEFT, padx=5)

    polis_frame = tk.Frame(new_window, background='lightblue')
    polis_frame.pack(pady=5)
    tk.Label(polis_frame, text="Полис", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.polis_entry = tk.Entry(polis_frame, width=15, font=("Arial", 12))
    root.polis_entry.pack(side=tk.LEFT, pady=5)

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=50)
    tk.Button(new_window, text="Зарегистрироваться",width=20, font=("Arial", 16),command=registration).pack()

def open_auto():
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Авторизация")
    new_window.geometry("300x500")

    tk.Label(new_window,
             text="Авторизация",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)

    surname_frame = tk.Frame(new_window, background='lightblue')
    surname_frame.pack(pady=5)
    tk.Label(surname_frame, text="Фамилия", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.surname_entry = tk.Entry(surname_frame, width=15, font=("Arial", 12))
    root.surname_entry.pack(side=tk.LEFT, padx=5)

    name_frame = tk.Frame(new_window, background='lightblue')
    name_frame.pack(pady=5)
    tk.Label(name_frame, text="Имя", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.name_entry = tk.Entry(name_frame, width=15, font=("Arial", 12))
    root.name_entry.pack(side=tk.LEFT, padx=5)

    patronymic_frame = tk.Frame(new_window, background='lightblue')
    patronymic_frame.pack(pady=5)
    tk.Label(patronymic_frame, text="Отчество", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.patronymic_entry = tk.Entry(patronymic_frame, width=15, font=("Arial", 12))
    root.patronymic_entry.pack(side=tk.LEFT, padx=5)

    polis_frame = tk.Frame(new_window, background='lightblue')
    polis_frame.pack(pady=5)
    tk.Label(polis_frame, text="Полис", background='lightblue', font=("Arial", 16)).pack(side=tk.LEFT)

    root.polis_entry = tk.Entry(polis_frame, width=15, font=("Arial", 12))
    root.polis_entry.pack(side=tk.LEFT, pady=5)

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=50)
    tk.Button(new_window, text="Авторизоваться",width=20, font=("Arial", 16),command=auto).pack()


def open_auto_window(result):
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Запись на прием")
    new_window.geometry("600x600")

    tk.Label(new_window,
             text=f"Добрый день,{result[1]}!",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)


    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=50)
    tk.Button(new_window, text="Записаться на прием",width=20, font=("Arial", 16),command=make_an_appointment_with_a_doctor).pack()

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=10)
    tk.Button(new_window, text="Наши врачи",width=20, font=("Arial", 16),command=doctor_window).pack()

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=10)
    tk.Button(new_window, text="Времена приема",width=20, font=("Arial", 16),command=doctor_and_time_window).pack()


def make_an_appointment_with_a_doctor():
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Запись к врачу")
    new_window.geometry("300x500")

    tk.Label(new_window,
             text="Запись",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)

    specialization_frame = tk.Frame(new_window, background='lightblue')
    specialization_frame.pack(pady=10)

    tk.Label(specialization_frame, text="Специализация:", background='lightblue', font=("Arial", 14)).pack()

    try:
        cursor.execute("SELECT name FROM Specializations")
        specializations = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить специализации: {str(e)}")
        specializations = []

    specialization_combo = ttk.Combobox(
        specialization_frame,
        values=specializations,
        font=("Arial", 12),
        width=28,
        state="readonly"
    )
    specialization_combo.pack(pady=5)
    specialization_combo.set("Выберите специализацию")

    doctor_frame = tk.Frame(new_window, background='lightblue')
    doctor_frame.pack(pady=10)

    tk.Label(doctor_frame, text="Врач:", background='lightblue', font=("Arial", 14)).pack()

    def update_doctors(event):
        selected_specialization = specialization_combo.get()
        try:
            cursor.execute("""SELECT d.name, d.surname, d.patronymic 
                           FROM Doctors d
                           JOIN Specializations s ON d.specialization_id = s.id
                           WHERE s.name = ?""", (selected_specialization,))
            doctors = [f"{row[1]} {row[0]} {row[2]}" for row in cursor.fetchall()]
            root.doctor_combo['values'] = doctors
            if doctors:
                root.doctor_combo.set("Выберите врача")
            else:
                root.doctor_combo.set("Нет доступных врачей")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить врачей: {str(e)}")
            root.doctor_combo['values'] = []
            root.doctor_combo.set("Ошибка загрузки")

    specialization_combo.bind("<<ComboboxSelected>>", update_doctors)

    root.doctor_combo = ttk.Combobox(
        doctor_frame,
        values=[],
        font=("Arial", 12),
        width=28,
        state="readonly"
    )
    root.doctor_combo.pack(pady=5)
    root.doctor_combo.set("Сначала выберите специализацию")

    time_frame = tk.Frame(new_window, background='lightblue')
    time_frame.pack(pady=10)

    tk.Label(time_frame, text="Время:", background='lightblue', font=("Arial", 14)).pack()

    def update_time(event):
        selected_doctor = root.doctor_combo.get()
        if not selected_doctor or selected_doctor == "Нет доступных врачей":
            return

        try:
            parts = selected_doctor.split()
            if len(parts) != 3:
                raise ValueError("Неверный формат ФИО врача")

            surname, name, patronymic = parts

            cursor.execute("""
                SELECT d.id, h.start_hour, h.finish_hour 
                FROM Doctors d
                JOIN Hours h ON d.time_id = h.id
                WHERE d.name = ? AND d.surname = ? AND d.patronymic = ?
            """, (name, surname, patronymic))

            doctor_data = cursor.fetchone()
            if not doctor_data:
                raise ValueError("Врач не найден")

            doctor_id, start_hour, finish_hour = doctor_data

            # Получаем доступное время, исключая уже занятые
            cursor.execute("""
                SELECT rh.time 
                FROM Reception_hours rh
                WHERE rh.time BETWEEN ? AND ?
                AND rh.id NOT IN (
                    SELECT mr.time_id 
                    FROM Medical_receptions mr
                    WHERE mr.doctor_id = ?
                )
            """, (start_hour, finish_hour, doctor_id))

            available_times = [f"{row[0]}" for row in cursor.fetchall()]

            root.time_combo['values'] = available_times
            if available_times:
                root.time_combo.set("Выберите время")
            else:
                root.time_combo.set("Нет доступного времени")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить время: {str(e)}")
            root.time_combo['values'] = []
            root.time_combo.set("Ошибка загрузки")

    root.doctor_combo.bind("<<ComboboxSelected>>", update_time)

    root.time_combo = ttk.Combobox(
        time_frame,
        values=[],
        font=("Arial", 12),
        width=28,
        state="readonly"
    )
    root.time_combo.pack(pady=5)
    root.time_combo.set("Сначала выберите врача")

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=50)
    tk.Button(new_window, text="Записаться", width=20, font=("Arial", 16), command=receptions).pack()

def doctor_window():
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Все врачи")
    new_window.geometry("300x500")

    tk.Label(new_window,
             text="Врачи",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)

    specialization_frame = tk.Frame(new_window, background='lightblue')
    specialization_frame.pack(pady=10)

    tk.Label(specialization_frame, text="Специализация:", background='lightblue', font=("Arial", 14)).pack()

    try:
        cursor.execute("SELECT name FROM Specializations")
        specializations = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить специализации: {str(e)}")
        specializations = []

    specialization_combo = ttk.Combobox(
        specialization_frame,
        values=specializations,
        font=("Arial", 12),
        width=28,
        state="readonly"
    )
    specialization_combo.pack(pady=5)
    specialization_combo.set("Выберите специализацию")
    def update_doctors():
        selected_specialization = specialization_combo.get()
        cursor.execute("""SELECT d.name, d.surname, d.patronymic 
                           FROM Doctors d
                           JOIN Specializations s ON d.specialization_id = s.id
                           WHERE s.name = ?""", (selected_specialization,))
        doctors = [f"{row[1]} {row[0]} {row[2]}" for row in cursor.fetchall()]
        if doctors:
            text = ""
            for d in doctors:
                text += d + '\n'
            result_label.config(text=text)


    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=10)
    tk.Button(new_window, text="Показать врачей", width=20, font=("Arial", 16), command=update_doctors).pack()
    result_label = tk.Label(new_window, text="", font=('Arial', 14), fg='black', background='lightblue')
    result_label.pack(pady=20)


def doctor_and_time_window():
    new_window = tk.Toplevel(root, background='lightblue')
    new_window.title("Все время")
    new_window.geometry("300x500")

    tk.Label(new_window,
             text="Врачи",
             font=("Arial", 24),
             background='lightblue').pack(pady=20)

    specialization_frame = tk.Frame(new_window, background='lightblue')
    specialization_frame.pack(pady=10)

    tk.Label(specialization_frame, text="Специализация:", background='lightblue', font=("Arial", 14)).pack()

    try:
        cursor.execute("SELECT name FROM Specializations")
        specializations = [row[0] for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить специализации: {str(e)}")
        specializations = []

    specialization_combo = ttk.Combobox(
        specialization_frame,
        values=specializations,
        font=("Arial", 12),
        width=28,
        state="readonly"
    )
    specialization_combo.pack(pady=5)
    specialization_combo.set("Выберите специализацию")

    def update_doctors():
        selected_specialization = specialization_combo.get()
        if not selected_specialization or selected_specialization == "Выберите специализацию":
            messagebox.showwarning("Ошибка", "Выберите специализацию!")
            return

        try:
            # Получаем всех врачей выбранной специализации
            cursor.execute("""
                SELECT d.surname, d.name, d.patronymic, h.start_hour, h.finish_hour
                FROM Doctors d
                JOIN Specializations s ON d.specialization_id = s.id
                JOIN Hours h ON d.time_id = h.id
                WHERE s.name = ?
            """, (selected_specialization,))

            doctors = cursor.fetchall()

            if not doctors:
                result_label.config(text="Нет врачей данной специализации")
                return

            text = ""
            for doctor in doctors:
                surname, name, patronymic, start_hour, finish_hour = doctor
                text += f"{surname} {name[0]}.{patronymic[0]}.: {start_hour}-{finish_hour}\n"

            result_label.config(text=text)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            result_label.config(text="Ошибка загрузки данных")

    buttons_frame = tk.Frame(new_window, background='lightblue')
    buttons_frame.pack(pady=10)
    tk.Button(new_window, text="Показать врачей", width=20, font=("Arial", 16), command=update_doctors).pack()

    result_label = tk.Label(new_window, text="", font=('Arial', 14), fg='black', background='lightblue',
                            justify=tk.LEFT)
    result_label.pack(pady=20)

def registration():
    name = root.name_entry.get()
    surname = root.surname_entry.get()
    patronymic = root.patronymic_entry.get()
    polis = root.polis_entry.get()
    if not all([surname, name, patronymic, polis]):
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
        return
    if len(polis) != 16 or polis.isdigit() == False:
        messagebox.showwarning("Ошибка", "Неверно введен полис!")
        return
    cursor.execute("INSERT INTO Patients (name, surname, patronymic, polis) VALUES(?,?,?,?)", (name, surname, patronymic, hash_password(polis)))
    conn.commit()
    messagebox.showinfo("Успех", "Пациент успешно зарегистрирован!")

def auto():
    global au_name, au_surname, au_patronymic, au_polis
    au_name = root.name_entry.get()
    au_surname = root.surname_entry.get()
    au_patronymic = root.patronymic_entry.get()
    au_polis = root.polis_entry.get()
    if not all([au_name, au_surname, au_patronymic, au_polis]):
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены!")
        return
    if len(au_polis) != 16 or au_polis.isdigit() == False:
        messagebox.showwarning("Ошибка", "Неверно введен полис!")
        return
    cursor.execute("SELECT * FROM Patients WHERE name = ? AND surname = ? AND patronymic = ? AND polis = ?", (au_name, au_surname, au_patronymic, hash_password(au_polis)))
    res = cursor.fetchone()
    if res:
        messagebox.showinfo("Успех", "Пациент авторизирован!")
        open_auto_window(res)
    else:
        messagebox.showwarning("Ошибка", "Пользователь не найден!")


def receptions():
    doctor = root.doctor_combo.get()  # Получаем выбранного врача
    time = root.time_combo.get()  # Получаем выбранное время

    if not doctor or doctor == "Сначала выберите специализацию" or doctor == "Нет доступных врачей":
        messagebox.showwarning("Ошибка", "Выберите врача!")
        return

    if not time or time == "Сначала выберите врача" or time == "Нет доступного времени":
        messagebox.showwarning("Ошибка", "Выберите время!")
        return

    try:
        doctor_parts = doctor.split()
        if len(doctor_parts) != 3:
            raise ValueError("Неверный формат ФИО врача")

        surname, name, patronymic = doctor_parts

        cursor.execute("""
            SELECT id
            FROM Patients
            WHERE name = ? AND surname = ? AND patronymic = ? AND polis = ?
        """, (au_name, au_surname, au_patronymic, hash_password(au_polis)))
        patient = cursor.fetchone()

        if not patient:
            messagebox.showerror("Ошибка", "Пациент не найден!")
            return

        patient_id = patient[0]

        cursor.execute("""
            SELECT id
            FROM Doctors
            WHERE name = ? AND surname = ? AND patronymic = ?
        """, (name, surname, patronymic))
        doctor = cursor.fetchone()

        if not doctor:
            messagebox.showerror("Ошибка", "Врач не найден!")
            return

        doctor_id = doctor[0]


        cursor.execute("""
            SELECT id
            FROM Reception_hours
            WHERE time = ?
        """, (time,))
        time_rec = cursor.fetchone()

        if not time_rec:
            messagebox.showerror("Ошибка", "Время приема не найдено!")
            return

        time_id = time_rec[0]

        cursor.execute("""
            INSERT INTO Medical_receptions (doctor_id, patient_id, time_id)
            VALUES (?, ?, ?)
        """, (doctor_id, patient_id, time_id))

        conn.commit()
        messagebox.showinfo("Успех", "Вы успешно записаны на прием!")

    except Exception as e:
        conn.rollback()
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")





title_frame = tk.Frame(root, bg='lightblue')
title_frame.pack(pady=50)
tk.Label(title_frame,text="Добро Пожаловать!!!",bg='lightblue',font=("Arial", 30)).pack()

buttons_frame = tk.Frame(root, bg='lightblue')
buttons_frame.pack(pady=20)

reg_frame = tk.Frame(buttons_frame, bg='lightblue')
reg_frame.pack(pady=10)
tk.Button(buttons_frame, text="Регистрация", font=("Arial", 12), padx=10, pady=5, width=20, command=open_registration).pack(side=tk.LEFT, padx=10)

auth_frame = tk.Frame(buttons_frame, bg='lightblue')
auth_frame.pack()
tk.Button(buttons_frame, text="Авторизация", font=("Arial", 12), padx=10, pady=5, width=20, command=open_auto).pack(side=tk.LEFT)

root.mainloop()