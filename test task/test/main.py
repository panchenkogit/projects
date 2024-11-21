from classes.library import Library


def main():
    print("================================")
    print("Добро пожаловать в библиотеку!")
    print("================================")
    library = Library()

    while True:
        print("\nВыберите действие:")
        print("1. Показать все книги")
        print("2. Найти книгу по ID")
        print("3. Найти книги автора")
        print("4. Найти книги по году")
        print("5. Добавить книгу")
        print("6. Удалить книгу")
        print("7. Обновить данные книги")
        print("0. Выход")

        try:
            choice = int(input("\nВведите номер действия: "))
        except ValueError:
            print("Ошибка: введите корректный номер.")
            continue

        if choice == 0:
            print("================================")
            print("Спасибо за использование библиотеки!")
            print("================================")
            break

        elif choice == 1:
            library.get_books()

        elif choice == 2:
            try:
                book_id = int(input("Введите ID книги: "))
                library.get_book_of_id(book_id)
            except ValueError:
                print("Ошибка: ID должен быть числом!")

        elif choice == 3:
            author = input("Введите имя автора: ")
            library.get_book_of_author(author)

        elif choice == 4:
            try:
                year = int(input("Введите год издания: "))
                library.get_book_of_year(year)
            except ValueError:
                print("Ошибка: Год должен быть числом!")

        elif choice == 5:
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            try:
                year = int(input("Введите год издания: "))
            except ValueError:
                print("Ошибка: Год должен быть числом!")
                continue
            status = (
                input("Введите статус книги (по умолчанию 'В наличии'): ")
                or "В наличии"
            )
            library.add_book(title, author, year, status)

        elif choice == 6:
            try:
                book_id = int(input("Введите ID книги для удаления: "))
                library.delete_book(book_id)
            except ValueError:
                print("Ошибка: ID должен быть числом!")

        elif choice == 7:
            try:
                book_id = int(input("Введите ID книги для обновления: "))
                title = input("Введите новое название книги: ")
                author = input("Введите нового автора книги: ")
                year = int(input("Введите новый год издания: "))
                status = input("Введите новый статус книги: ")
                library.update_book(book_id, title, author, year, status)
            except ValueError:
                print("Ошибка: Неверный ввод данных!")

        else:
            print("Ошибка: выберите действие из списка.")


if __name__ == "__main__":
    main()
