import os
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        self.balance += amount
        self.history.append(f" Пополнение: + {amount}")
        print()
        print(f"Баланс обновлен: {self.balance}")
        print(f"Пополнение на: {amount}")


    def withdraw(self, amount):
        if self.balance < amount:
            print("Недостаточно средств")
        else:
            self.balance -= amount
            self.history.append(f"Снятие: - {amount}")
            print("Средства сняты")


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
    print("\n=== Банк ===")
    print("1. Пополнить счёт")
    print("2. Снять деньги")
    print("3. Показать баланс")
    print("4. Выйти")
    print("5. История операций")


    choice = input("Выберите: ")

    if choice == "1":
        x = int(input("Введите сумму пополнения: "))
        user.deposit(x)
    elif choice == "2":
        x = int(input("Введите сумму снятия: "))
        user.withdraw(x)
    elif choice == "3":
        user.show_balance()
    elif choice == "4":
        user.save_to_file()
        print("Данные сохранены в bank.txt")
        break
    elif choice == "5":
        for record in user.history:
            print(record)


