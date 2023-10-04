import pickle
from abc import ABC, abstractmethod


class Contact(ABC):
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    @abstractmethod
    def get_contact_info(self):
        pass


class PersonalContact(Contact):
    def get_contact_info(self):
        return f"Ім'я: {self.name}, Телефон: {self.phone}"


class BusinessContact(Contact):
    def __init__(self, name, phone, company):
        super().__init__(name, phone)
        self.company = company

    def get_contact_info(self):
        return f"Ім'я: {self.name}, Телефон: {self.phone}, Компанія: {self.company}"


class AddressBook:
    def __init__(self):
        self.contacts = []

    def add_contact(self, contact):
        self.contacts.append(contact)

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.contacts, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.contacts = pickle.load(file)
        except FileNotFoundError:
            pass

    def search_contacts(self, search_term):
        results = []
        for contact in self.contacts:
            if (search_term.lower() in contact.name.lower()) or (search_term in contact.phone):
                results.append(contact)
        return results

    def display_all_contacts(self):
        if self.contacts:
            print("Список контактів:")
            for contact in self.contacts:
                print(contact.get_contact_info())
        else:
            print("Адресна книга порожня.")


# Основна частина програми
def main():
    address_book = AddressBook()

    try:
        address_book.load_from_file('address_book.pkl')
    except FileNotFoundError:
        pass

    while True:
        print("1. Додати контакт")
        print("2. Знайти контакт")
        print("3. Вивести список всіх контактів")
        print("4. Вийти")

        choice = input("Виберіть дію: ")

        if choice == '1':
            name = input("Введіть ім'я контакту: ")
            phone = input("Введіть номер телефону контакту: ")
            contact_type = input("Введіть тип контакту (personal/business): ").lower()

            if contact_type == 'personal':
                contact = PersonalContact(name, phone)
            elif contact_type == 'business':
                company = input("Введіть назву компанії: ")
                contact = BusinessContact(name, phone, company)
            else:
                print("Невідомий тип контакту. Контакт не було додано.")
                continue

            address_book.add_contact(contact)
            address_book.save_to_file('address_book.pkl')
            print("Контакт додано!")

        elif choice == '2':
            search_term = input("Введіть рядок для пошуку: ")
            results = address_book.search_contacts(search_term)
            if results:
                print("Знайдені контакти:")
                for contact in results:
                    print(contact.get_contact_info())
            else:
                print("Контакти не знайдені.")

        elif choice == '3':
            address_book.display_all_contacts()

        elif choice == '4':
            break


if __name__ == "__main__":
    main()
