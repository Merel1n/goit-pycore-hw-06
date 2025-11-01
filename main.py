from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if len(value) > 2 or not value.isdigit():
            return "The name must be more than two characters and not contain numbers."
        self.value = value

"""
Клас Phone:

﻿Реалізовано валідацію номера телефону (має бути перевірка на 10 цифр).

"""
class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            return "Invalid phone number format. Must be in format +<country_code><number>"
        super().__init__(value)  
    
    @staticmethod
    def validate(value):
        # паревірка номеру телефону щоб мав формат "+(код країни)10цифр"
        return value.startswith("+") or not value[1:].isdigit() and len(value) >= 10
    
"""
Клас Record:

Реалізовано зберігання об'єкта Name в окремому атрибуті.
Реалізовано зберігання списку об'єктів Phone в окремому атрибуті.
Реалізовано методи для додавання - add_phone/видалення - remove_phone/редагування - edit_phone/пошуку об'єктів Phone - find_phone.
"""
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
    
    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, name):
        for p in self.names:
            if p.value == name:
                return p
        return None
    
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
"""
Клас AddressBook:

Реалізовано метод add_record, який додає запис до self.data.
Реалізовано метод find, який знаходить запис за ім'ям.
Реалізовано метод delete, який видаляє запис за ім'ям.
"""
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
    return inner

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    name = name.strip().lower()
    if not phone.startswith("+") or not phone[1:].isdigit():
        return "Invalid phone number format. Must be in format +<country_code><number>"
    contacts[name] = phone
    return "Contact added."

@input_error
def change_contact(args, contacts):
    if not args:
        return "No name provided"
    name = args[0]
    phone = args[1]
    if not phone.startswith("+") or not phone[1:].isdigit():
        return "Invalid phone number format. Must be in format +<country_code><number>"
    name = name.strip().lower()
    if name in contacts:
        contacts[name] = phone
        return "Contact updated."
    else:
        raise KeyError

@input_error
def show_phone (args, contacts):
    name = args[0]
    name = name.strip().lower()
    if name in contacts:
        return f"Phone number for {name.capitalize()}: {contacts[name]}"
    else:
        raise KeyError


@input_error
def all_contact(contacts):
    if not contacts:
        return "No contacts found."
    result = "Contacts:\n"
    for name, phone in contacts.items():
        display_name = name.capitalize()
        result += f"{display_name}: {phone}\n"
    return result

def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(all_contact(contacts))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()