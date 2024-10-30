#Розробіть систему для управління адресною книгою.

from collections import UserDict
import re
from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            # Додайте перевірку коректності даних та перетворіть рядок на об'єкт datetime
            self.birthday = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Field:
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, name):
        super().__init__(name)


""" валідацію номера телефону (має бути перевірка на 10 цифр) """
class Phone(Field):
    def __init__(self, phone):
        self.phone = phone
        super().__init__(phone)
        if not self.__validate():
            raise ValueError("Invalid phone format. Expected 10 ")


    def __validate (self) -> bool:
         return bool(re.fullmatch(r'\d{10}', self.phone))
         

"""Реалізовано зберігання об'єкта Name в окремому атрибуті.
Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
Реалізовано методи для додавання - add_phone/видалення - remove_phone/редагування - 
edit_phone/пошуку об'єктів Phone - find_phone.
"""
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def __str__(self):
        birthday = datetime.strftime(self.birthday.birthday, "%d.%m.%Y") if self.birthday != None else "No info"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, \
birthday: {birthday}"


    def add_birthday(self, birthday : str):
        birth_date = Birthday(birthday)
        self.birthday = birth_date


    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))


    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return "Phone removed."
        return "Phone not found."


    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return "Phone updated."
        return "Phone not found."


    def find_phone(self, phone: str) -> str:
        for p in self.phones:
            if p.value == phone:
                return p.value
        return "Phone not found."


    def copy_record(self):
        result = Record(self.name)

        result.phones = self.phones
        result.birthday = Birthday(self.birthday.birthday.strftime("%d.%m.%Y"))

        return result


class AddressBook(UserDict):
    def add_record (self, record : Record):
        self.data[record.name.value] = record #,  додає запис до self.data.
    

    def find(self, name : str): #,  знаходить запис за ім'ям.
        return self.data.get(name, "Record not found.")


    def get_upcoming_birthdays(self):
    
        today = datetime.today().date()

        users_to_congrat = AddressBook()

        try :
            for title in self.data:
                user = self.data[title]
                if user.birthday != None:
                    user_birthday = user.birthday.birthday
            
                    # Empoyee's birthday this year
                    user_birthday = user_birthday.replace(year=today.year)
            
                    # NewYear case
                    if (user_birthday < today) : 
                        user_birthday = user_birthday.replace(year=today.year + 1)

                    # How many days before birthday
                    days_before = (user_birthday - today).days
                    
                    # If current week
                    if (0<= days_before <= 7) :
                        # If on weekends 
                        if (user_birthday.weekday() >=5) :
                            user_birthday += timedelta(days=(7 -user_birthday.weekday()))

                        temp = user.copy_record()
                        temp.add_birthday(user_birthday.strftime("%d.%m.%Y"))
                        users_to_congrat.add_record(temp)
            return users_to_congrat
            
        except:
            print("Error")
            return self


    def delete(self, name : str): # видаляє запис за ім'ям.
        if name in self.data:
            del self.data[name]
            return "Record deleted."
        return "Record not found."



# # Створення нової адресної книги
# book = AddressBook()

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)
# jane_record.add_birthday("1999.11.03")

# jin_record = Record("Jine")
# jin_record.add_phone("9876543210")
# book.add_record(jin_record)
# jin_record.add_birthday("1999.11.23")

# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")
# john.add_birthday("1999.10.30")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# birthday_book = AddressBook()
# birthday_book = book.get_upcoming_birthdays()
# for el in birthday_book:
#     print(el)

# # Видалення запису Jane
# book.delete("Jane")