from collections import UserDict


class Field:
    """Базовий клас для полів запису"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Клас для зберігання імені контакту"""
    def __init__(self, value):
        if not self.validate(value):
            return "The name must be more than two characters and not contain numbers."
        self.value = value
    @staticmethod
    def validate(value):
        """Перевіряє, що ім'я більше 2 символів і не складається з цифер"""
        return len(value) > 2 or not value.isdigit()


class Phone(Field):
    """Клас для зберігання номера телефону з валідацією"""
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        """паревірка номеру телефону щоб мав формат "+(код країни)10цифр"""
        return (value.startswith("+") or not value[1:].isdigit()) and len(value[1:]) >= 10


class Record:
    """Клас для зберігання інформації про контакт"""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        """Додає новий номер телефону"""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Видаляє телефон за номером"""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        """Редагує існуючий номер телефону"""
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone):
        """Повертає телефон, якщо він є у списку"""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        """Гарне текстове представлення запису"""
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        return f"Contact name: {self.name.value}, phones: {phones_str}"


class AddressBook(UserDict):
    """Клас для зберігання та управління записами"""
    def add_record(self, record):
        """Додає новий запис у книгу"""
        self.data[record.name.value] = record

    def find(self, name):
        """Знаходить запис за ім’ям"""
        return self.data.get(name)

    def delete(self, name):
        """Видаляє запис за ім’ям"""
        if name in self.data:
            del self.data[name]

if __name__ == "__main__":
# Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("+1234567890")
    john_record.add_phone("+5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("+9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("+1234567890", "+1112223333")

    print(john)  # Виведення: Contact name: John, phones: +1112223333; +5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("+5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: +5555555555

    # Видалення запису Jane
    book.delete("Jane")
