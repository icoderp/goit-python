from mongoengine import DoesNotExist, MultipleObjectsReturned
from mongoengine.queryset.visitor import Q
from models import Contact


class ExceptError:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        try:
            return self.func(*args)
        except DoesNotExist as err:
            print(err)
        except MultipleObjectsReturned as err:
            print(f'Write first name, last name for searching.\nErrors - {err}')
        except Exception as err:
            print(err)


@ExceptError
def bd_create_contact(first_name, last_name, phone):
    Contact(first_name=first_name, last_name=last_name, phone=phone).save()


@ExceptError
def db_change_phone(first_name, last_name, phone):
    contact = Contact.objects(Q(name=first_name) & Q(last_name=last_name))
    contact.update(phone=phone)


@ExceptError
def bd_delete_phone(first_name, last_name):
    contact = Contact.objects(Q(name=first_name) & Q(last_name=last_name))
    contact.update(phone='None')


@ExceptError
def bd_update_birthday(first_name, last_name, birthday):
    contact = Contact.objects(Q(name=first_name) & Q(last_name=last_name))
    contact.update(birthday=birthday)


@ExceptError
def bd_show_birthday(first_name, last_name):
    contact = Contact.objects.get(Q(name=first_name) & Q(last_name=last_name))
    birthday = contact.birthday
    return birthday


@ExceptError
def db_show_phone(first_name, last_name):
    contact = Contact.objects.get(Q(name=first_name) & Q(last_name=last_name))
    phone = contact.phone
    return phone


@ExceptError
def bd_delete_phone(first_name, last_name):
    contact = Contact.objects(Q(name=first_name) & Q(last_name=last_name))
    contact.update(phone='None')


@ExceptError
def bd_delete_all():
    Contact.objects.delete()

