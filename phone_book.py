
from collections import UserDict

class Field:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Field value must be a string")

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self):
        return self.value


class Name(Field):
    def __init__(self, value: str):
        super().__init__(value)

        if not value.strip():
            raise ValueError("Name cannot be empty")

    @property
    def key(self) -> str:
        return self.value.casefold()


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)

        if len(value) != 10 or not value.isascii() or not value.isdigit():
            raise ValueError("Phone number must contain exactly 10 digits")


class Record:
    def __init__(self, name: str):
        self._name = Name(name)
        self._phones = []

    @property
    def name(self) -> Name:
        return self._name

    @property
    def phones(self) -> tuple:
        return tuple(self._phones)

    def add_phone(self, phone: str):
        self._phones.append(Phone(phone))

    def find_phone(self, phone: str):
        for phone_obj in self._phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def remove_phone(self, phone: str):
        found_phone = self.find_phone(phone)

        if found_phone is not None:
            self._phones.remove(found_phone)

    def edit_phone(self, old_phone: str, new_phone: str):
        found_phone = self.find_phone(old_phone)

        if found_phone is None:
            raise ValueError(f"Phone number {old_phone} not found")

        new_phone_obj = Phone(new_phone)
        index = self._phones.index(found_phone)
        self._phones[index] = new_phone_obj

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self._phones)}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.key] = record

    def find(self, name: str):
        return self.data.get(name.casefold())

    def delete(self, name: str):
        self.data.pop(name.casefold(), None)


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")

    if john:
        john.edit_phone("1234567890", "1112223333")

        print(john)

        found_phone = john.find_phone("5555555555")
        if found_phone:
            print(f"{john.name}: {found_phone}")

    book.delete("Jane")

    for name, record in book.data.items():
        print(record)
