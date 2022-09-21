import datetime
import re
from datetime import date
import phonenumbers
from abc import ABC, abstractmethod
# from src.func import *


class Field(ABC):
    def __init__(self, value):
        self.value = value
        self.__value = None

    def __repr__(self):
        return f'{self.value}'

    def __str__(self) -> str:
        return f'{self.value}'

    def __eq__(self, other) -> bool:
        return self.value == other.value

    @abstractmethod
    def value(self):
        ...


class FirstName(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class LastName(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            number = phonenumbers.parse(value, "ITU-T")
            self.__value = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            print("Enter correct number, for example +380987654321")
            raise ValueError


class Birthday(Field):
    def __str__(self):
        if self.value is None:
            return 'Unknown'
        else:
            return f'{self.value:%d %b %Y}'

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value is None:
            self.__value = None
        else:
            try:
                self.__value = datetime.datetime.strptime(value, '%d.%m.%Y').date()
            except ValueError:
                print("Enter the date of birth (dd.mm.yyyy)")


class Address(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value.title()


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        result = None
        get_email = re.findall(r'\b[a-zA-Z][\w\.]+@[a-zA-Z]+\.[a-zA-Z]{2,}', value)
        for i in get_email:
            result = i
        if result is None:
            raise AttributeError(f" Email is not correct {value}")
        self.__value = result


class Record:
    def __init__(self, first_name: FirstName, last_name=None, phones=None, birthday=None, email=None, address=None) -> None:
        if phones is None:
            phones = []
        self.first_name = first_name
        self.last_name = last_name
        self.phone_list = phones
        self.birthday = birthday
        self.address = address
        self.email = email

    def __str__(self) -> str:
        return f' Contact:  {self.first_name.value.title()} {self.last_name.value}\n' \
               f' Phones:   {", ".join([phone.value for phone in self.phone_list])}\n' \
               f' Birthday: {self.birthday}\n' \
               f' Email:    {self.email}\n' \
               f' Address:  {self.address}'

    def add_phone(self, phone: Phone) -> None:
        self.phone_list.append(phone)

    def del_phone(self, phone: Phone) -> None:
        self.phone_list.remove(phone)

    def edit_phone(self, phone: Phone, new_phone: Phone) -> None:
        self.phone_list.remove(phone)
        self.phone_list.append(new_phone)

    @staticmethod
    def days_to_birthday(self, birthday: Birthday):
        if birthday.value is None:
            return None
        this_day = date.today()
        birthday_day = date(this_day.year, birthday.value.month, birthday.value.day)
        if birthday_day < this_day:
            birthday_day = date(this_day.year + 1, birthday.value.month, birthday.value.day)
        return (birthday_day - this_day).days


class InputError:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except IndexError:
            return 'Error! Print correct data!'
        except KeyError:
            return 'Error! User not found!'
        except ValueError:
            return 'Error! Data is incorrect!'
        except AttributeError:
            return "Enter correct the date of birth (dd.mm.yyyy) for this user"


def greeting(*args):
    return 'Hello! How can I help you?'


@InputError
def add_contact(*args):
    ...


@InputError
def change_contact(*args):
    ...


@InputError
def show_all(*args):
    ...


@InputError
def del_phone(*args):
    ...


@InputError
def add_birthday(*args):
    ...


@InputError
def user_birthday(*args):
    ...


@InputError
def show_phone(*args):
    ...


@InputError
def del_user(*args):
    ...


@InputError
def clear_all(*args):
    ...


@InputError
def add_email(*args):
    ...


@InputError
def add_address(*args):
    ...


@InputError
def add_last_name(*args):
    ...


@InputError
def find(*args):
    ...


def info():
    return """
    *********** Service command ***********
    "help", "?"          --> Commands list
    "close", "exit", "." --> Exit from AddressBook

    *********** Add/edit command **********
    "add" name last name  phone                  --> Add user to AddressBook
    "change" name last name  new_phone --> Change the user's phone number
    "birthday" name last name birthday          --> Add/edit user birthday
    "email" name last name email                --> Add/edit user email
    "last name" name last name        --> Add/edit user last name
    "address" name last name address            --> Add/edit user address

    *********** Delete command ***********
    "del" name last name --> Delete phone number
    "delete" name last name    --> Delete user
    "clear"          --> Delete all users

    *********** Info command *************
    "show" name last name          --> Show user info
    "show all"           --> Show all users info
    "user birthday" name last name  --> Show how many days to user birthday
    "find" data          --> Find any data 
    """


def exiting():
    return 'Good bye!'


def unknown_command(*args):
    return 'Unknown command! Enter again!'


COMMANDS = {greeting: ['hello'],
            add_contact: ['add '],
            change_contact: ['change '],
            info: ['help', '?'],
            show_all: ['show all'],
            exiting: ['good bye', 'close', 'exit', '.'],
            del_phone: ['del '],
            add_birthday: ['birthday'],
            user_birthday: ['user birthday '],
            show_phone: ['show '],
            del_user: ['delete '],
            clear_all: ['clear'],
            add_email: ['email '],
            add_address: ['address'],
            add_last_name: ['last name'],
            find: ['find']}


def command_parser(user_command: str) -> (str, list):
    for key, list_value in COMMANDS.items():
        for value in list_value:
            if user_command.lower().startswith(value):
                args = user_command[len(value):].split()
                return key, args
    else:
        return unknown_command, []


def main():
    print(info())
    while True:
        user_command = input('Enter your command: >>> ')
        if user_command == 'exit':
            return 'Good bye!'
        command, data = command_parser(user_command)
        print(command(*data))
        if command is exiting:
            break


if __name__ == '__main__':
    main()
