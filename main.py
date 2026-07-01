from datetime import datetime
import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, 
        balance INTEGER DEFAULT 0
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        owner TEXT NOT NULL,
        record TEXT NOT NULL
    )
""")

conn.commit()

def create_user(users):
    name = input("Введите имя: ").strip()
    users[name] = BankAccount(name, 0)
    cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", (name, 0))
    conn.commit()
    return name

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            print("Сумма должна быть больше нуля!")
            return
        self.balance += amount
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.history.append(f"{time_now} Пополнение: + {amount}")
        print(f"\nБаланс обновлен: {self.balance}")


    def withdraw(self, amount):
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        if self.balance < amount:
            print(f"\nНедостаточно средств. На балансе: {self.balance}")
        else:
            self.balance -= amount
            self.history.append(f"{time_now} Снятие: - {amount}")
            print(f"{time_now} Средства сняты. Текущий баланс: {self.balance}")

    def transfer(self, amount, recipient):
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            time_now = datetime.now().strftime("%d.%m.%Y %H:%M")

            self.history.append(f"{time_now} Перевод пользователю: {recipient.owner}: - {amount}")
            recipient.history.append(f"{time_now} Получен перевод от {self.owner}: + {amount}")

            self.save_to_db()
            recipient.save_to_db()
            print("Перевод успешно выполнен!")
        else:
            print("Недостаточно средств для перевода!")


    def show_balance(self):
        print(f"Текущий баланс: {self.balance}")

    def save_to_db(self):
        cursor.execute("UPDATE users SET balance = ? WHERE name = ?", (self.balance, self.owner))

        cursor.execute("DELETE FROM history WHERE owner = ?", (self.owner,))
        for record in self.history:
            cursor.execute("INSERT INTO history (owner, record) VALUES (?, ?)", (self.owner, record))
        conn.commit()

    def load_from_db(self):
        cursor.execute("SELECT balance FROM users WHERE name = ?", (self.owner,))
        row = cursor.fetchone()
        if row:
            self.balance = row[0]

        cursor.execute("SELECT * FROM history WHERE owner = ?", (self.owner,))
        rows = cursor.fetchall()
        self.history = [row[2] for row in rows]


def create_user():
    name = input("Введите имя для регистрации: ").strip()
    try:
        cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", (name, 0))
        conn.commit()
        print(f"Пользователь {name} успешно зарегистрирован!")
        return BankAccount(name, 0)
    except sqlite3.IntegrityError:
        print("Пользователь с таким именем уже существует!")
        return None


def user_menu(current_user):
    while True:
        print(f"\n*** Кошелек, {current_user.owner} ***")
        print("1. Пополнение")
        print("2. Снятие")
        print("3. Показать баланс")
        print("4. Выйти из аккаунта (Сохранить)")
        print("5. История операций")
        print("6. Отправить деньги")

        choice = input("Выберите команду: ")

        if choice == "1":
            try:
                x = int(input("Введите сумму пополнения: "))
                current_user.deposit(x)
            except ValueError:
                print("Ошибка! Введите число.")
        elif choice == "2":
            try:
                x = int(input("Введите сумму снятия: "))
                current_user.withdraw(x)
            except ValueError:
                print("Ошибка! Введите число.")
        elif choice == "3":
            current_user.show_balance()
        elif choice == "4":
            current_user.save_to_db()
            print("Данные сохранены. Выход в главное меню.")
            break
        elif choice == "5":
            print("\n*** История операций ***")
            if not current_user.history:
                print("История пуста.")
            for record in current_user.history:
                print(record)
        elif choice == "6":
            rec_name = input("Имя получателя: ").strip()
            if rec_name == current_user.owner:
                print("Нельзя переводить деньги самому себе!")
                continue

            cursor.execute("SELECT * FROM users WHERE name = ?", (rec_name,))
            if cursor.fetchone():
                recipient = BankAccount(rec_name)
                recipient.load_from_db()
                try:
                    amount = int(input("Сумма перевода: "))
                    if amount <= 0:
                        print("Сумма должна быть больше нуля!")
                        continue
                    current_user.transfer(amount, recipient)
                except ValueError:
                    print("Ошибка! Введите числовое значение суммы.")
            else:
                print("Пользователь не найден!")

while True:
   print("\n *** Добро пожаловать в систему Банка ***")
   print("1. Войти в аккаунт")
   print("2. Регистрация нового пользователя")
   print("3. Выйти из системы")

   main_choice = input("Выберите команду: ")

   if main_choice == "1":
       name = input("Введите имя: ").strip()
       cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
       if cursor.fetchone():
           user = BankAccount(name)
           user.load_from_db()
           user_menu(user)
       else:
           print("Пользователь не найден!")

   elif main_choice == "2":
       user = create_user()
       if user:
           user_menu(user)

   elif main_choice == "3":
       print("Программа завершена.")
       break

conn.close()

