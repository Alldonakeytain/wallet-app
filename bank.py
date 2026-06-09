import os
from datetime import datetime

users = {}
current_user = None


def create_user(users):
    name = input("Введите имя: ").strip()
    users[name] = BankAccount(name, 0)
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

            recipient.save_to_file()
        else:
            print("Недостаточно средств!")


    def show_balance(self):
        print(f"Текущий баланс: {self.balance}")

    def save_to_file(self):
        with open(f"{self.owner}.txt", "w", encoding="utf-8") as f:
            f.write(f"Владелец: {self.owner}\n")
            f.write(f"Баланс: {self.balance}\n")
            f.write("История:\n")
            for record in self.history:
                f.write(record + "\n")

    def load_from_file(self):
        with open(f"{self.owner}.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.balance = int(lines[1].split(": ")[1])
            self.history = []
            for line in lines[3:]:
                self.history.append(line.strip())

while True:
    print("*** Добро пожаловать ***")
    print("1. Войти")
    print("2. Регистрация")

    choice = input("Выберите команду: ")
    if choice == "1":
        name = input("Введите имя: ").strip()
        if name in users or os.path.exists(f"{name}.txt"):
            if name not in users:
                users[name] = BankAccount(name, 0)
            current_user = users[name]
            current_user.load_from_file()
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
                current_user.save_to_file()
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
                if os.path.exists(f"{rec_name}.txt"):
                    recipient = BankAccount(rec_name, 0)
                    recipient.load_from_file()
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
                current_user.save_to_file()
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
                if os.path.exists(f"{rec_name}.txt"):
                    recipient = BankAccount(rec_name, 0)
                    recipient.load_from_file()
                    amount = int(input("Сумма перевода: "))
                    current_user.transfer(amount, recipient)
                else:
                    print("Пользователь не найден!")


