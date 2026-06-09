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

users = {}
current_user = None


def create_user(users):
    name = input("Введите имя: ").strip()
    users[name] = BankAccount(name, 0)
    cursor.execute("INSERT INTO users (name, balance) VALUES (?, ?)", (name, 0))
    conn.commit()
    return name

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        self.history.append(f"{time_now} Пополнение: + {amount}")

        print()
        print(f"Баланс обновлен: {self.balance}")
        print(f"{time_now} Пополнение на: + {amount}")


    def withdraw(self, amount):
        time_now = datetime.now().strftime("%d.%m.%Y %H:%M")
        if self.balance < amount:
            print()
            print("Недостаточно средств")
            print(f"На вашем балансе: {self.balance}")
        else:
            self.balance -= amount
            self.history.append(f"{time_now} Снятие: - {amount}")
            print(f"{time_now} Средства сняты")

    def transfer(self, amount, recipient):
        if self.balance >= amount:
            self.balance -= amount
            recipient.balance += amount
            time_now = datetime.now().strftime("%d.%m.%Y %H:%M")
            self.history.append(f"{time_now} Перевод: - {amount}")
            recipient.history.append(f"{time_now} Получен перевод: + {amount}")

            recipient.save_to_db()
        else:
            print("Недостаточно средств!")


    def show_balance(self):
        print(f"Текущий баланс: {self.balance}")


    def save_to_db(self):
        cursor.execute("UPDATE users SET balance = ? WHERE name = ?", (self.balance, self.owner))
        for record in self.history:
            cursor.execute("INSERT INTO history (owner, record) VALUES (?, ?)", (self.owner, record))

        conn.commit()


    def load_from_db(self):
        cursor.execute("SELECT balance FROM users WHERE name = ?", (self.owner,))
        row = cursor.fetchone()
        self.balance = row[0]

        cursor.execute("SELECT * FROM history WHERE owner = ?", (self.owner,))
        rows = cursor.fetchall()
        self.history = [row[2] for row in rows]


while True:
    print("*** Добро пожаловать ***")
    print("1. Войти")
    print("2. Регистрация")

    choice = input("Выберите команду: ")
    if choice == "1":
        name = input("Введите имя: ").strip()
        cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
        if cursor.fetchone():
            if name not in users:
                users[name] = BankAccount(name, 0)
            current_user = users[name]
            current_user.load_from_db()
        else:
            print("Пользователь не найден!")
            print()
            continue
        while True:
            print(f"\n*** Wallet, {name} ***")
            print("1. Пополнение")
            print("2. Снятие")
            print("3. Показать баланс")
            print("4. Выйти")
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
                print("Данные сохранены.")
                break
            elif choice == "5":
                print()
                print("*** История операций ***")
                for record in current_user.history:
                    print(record)
            elif choice == "6":
                print()
                rec_name = input(f"Имя получателя: ").strip()
                cursor.execute("SELECT * FROM users WHERE name = ?", (rec_name,))
                if cursor.fetchone():
                    recipient = BankAccount(rec_name, 0)
                    recipient.load_from_db()
                    amount = int(input("Сумма перевода: "))
                    current_user.transfer(amount, recipient)
                else:
                    print("Пользователь не найден!")

    elif choice == "2":
        name = create_user(users)
        current_user = users[name]
        while True:
            print("\n*** Wallet ***")
            print("1. Пополнение")
            print("2. Снятие")
            print("3. Показать баланс")
            print("4. Выйти")
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
                print("Данные сохранены.")
                break
            elif choice == "5":
                print()
                print("*** История операций ***")
                for record in current_user.history:
                    print(record)
            elif choice == "6":
                print()
                rec_name = input("Имя получателя: ").strip()
                cursor.execute("SELECT * FROM users WHERE name = ?", (rec_name,))
                if cursor.fetchone():
                    recipient = BankAccount(rec_name, 0)
                    recipient.load_from_db()
                    amount = int(input("Сумма перевода: "))
                    current_user.transfer(amount, recipient)
                else:
                    print("Пользователь не найден!")


