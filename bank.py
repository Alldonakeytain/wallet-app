import os
from datetime import datetime

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


    def show_balance(self):
        print(f"Текущий баланс: {self.balance}")

    def save_to_file(self):
        with open("bank.txt", "w", encoding="utf-8") as f:
            f.write(f"Владелец: {self.owner}\n")
            f.write(f"Баланс: {self.balance}\n")
            f.write("История:\n")
            for record in self.history:
                f.write(record + "\n")

    def load_from_file(self):
        with open("bank.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
            self.balance = int(lines[1].split(": ")[1])
            for line in lines[3:]:
                self.history.append(line.strip())

user = BankAccount("Макс", 0)


if os.path.exists("bank.txt"):  # если файл существует
    user.load_from_file()
    print("Данные загружены!")
else:
    user.balance = 1000  # первый запуск — стартовый баланс


while True:
    print("\n*** Wallet ***")
    print("1. Пополнение")
    print("2. Снятие")
    print("3. Показать баланс")
    print("4. Выйти")
    print("5. История операций")


    choice = input("Выберите команду: ")

    if choice == "1":
        try:
            x = int(input("Введите сумму пополнения: "))
            user.deposit(x)
        except ValueError:
            print("Ошибка! Введите число.")
    elif choice == "2":
        try:
            x = int(input("Введите сумму снятия: "))
            user.withdraw(x)
        except ValueError:
            print("Ошибка! Введите число.")
    elif choice == "3":
        user.show_balance()
    elif choice == "4":
        user.save_to_file()
        print("Данные сохранены в bank.txt")
        break
    elif choice == "5":
        print()
        print("*** История операций ***")
        for record in user.history:
            print(record)


