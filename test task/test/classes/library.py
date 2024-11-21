import json


class Library:
    def __init__(self, filename: str = "library.txt"):
        self.filename = filename
        self.books = self.load_books()

    """загрузка книг из файла"""

    def load_books(self):

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла! Файл поврежден, создаём новый.")
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump([], file, indent=4, ensure_ascii=False)
            return []

    """сохранение изменений в файл"""

    def save_books(self):

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)

        """вывод всех книг"""

    def get_books(self):

        if not self.books:
            print("В библиотеке пока нет книг.")
            return None
        print("Список книг:")
        for book in self.books:
            print(
                f"ID: {book['id']}\n"
                f"Название: {book['title']}\n"
                f"Автор: {book['author']}\n"
                f"Год: {book['year']}\n"
                f"Статус: {book['status']}\n"
            )
            print("*" * 20)

    """поиск книги по id"""

    def get_book_of_id(self, book_id: int) -> None:
        try:
            book_id = int(book_id)
        except ValueError:
            print("Ошибка: ID должен быть числом!")
            return None

        books_of_id = [book for book in self.books if book["id"] == book_id]
        if not books_of_id:
            print(f"Книга с ID {book_id} не найдена!")
            return None
        for book in books_of_id:
            print(
                f"ID: {book['id']}\n"
                f"Название: {book['title']}\n"
                f"Автор: {book['author']}\n"
                f"Год: {book['year']}\n"
                f"Статус: {book['status']}\n"
            )
            print("*" * 20)

        """поиск книг по автору"""

    def get_book_of_author(self, author: str) -> None:
        found_books = [book for book in self.books if book["author"] == author]
        if not found_books:
            print(f"Книги этого автора ({author}) не найдены!")
            return None

        for book in found_books:
            print(
                f"ID: {book['id']}\n"
                f"Название: {book['title']}\n"
                f"Автор: {book['author']}\n"
                f"Год: {book['year']}\n"
                f"Статус: {book['status']}\n"
            )
            print("*" * 20)

        """поиск книг по году"""

    def get_book_of_year(self, year: int) -> None:

        try:
            year = int(year)
        except ValueError:
            print("Ошибка: год должен быть числом!")
            return None

        books_of_year = [book for book in self.books if book["year"] == year]
        if not books_of_year:
            print(f"Книги за {year} год не найдены!")
            return None
        for book in books_of_year:
            print(
                f"ID: {book['id']}\n"
                f"Название: {book['title']}\n"
                f"Автор: {book['author']}\n"
                f"Год: {book['year']}\n"
                f"Статус: {book['status']}\n"
            )
            print("*" * 20)

        """добавление новой книги"""

    def add_book(
        self, title: str, author: str, year: int, status: str = "В наличии"
    ) -> None:

        try:
            year = int(year)
        except ValueError:
            print("Ошибка: год должен быть числом!")
            return None

        for book in self.books:
            if book["title"] == title and book["author"] == author:
                print("Такая книга уже есть в библиотеке!")
                return None

        new_book = {
            "id": len(self.books) + 1,
            "title": title,
            "author": author,
            "year": year,
            "status": status,
        }

        self.books.append(new_book)
        self.save_books()
        print("Книга добавлена успешно!")

    """удаление книги по id"""

    def delete_book(self, book_id: int) -> None:

        try:
            book_id = int(book_id)
        except ValueError:
            print("Ошибка: ID должен быть числом!")
            return None

        found_book = [book for book in self.books if book["id"] == book_id]
        if not found_book:
            print(f"Книга с ID {book_id} не найдена!")
            return None

        print(f"Книга с ID {book_id} удалена!")
        self.books.remove(found_book[0])
        self.save_books()

    """обновление данных книги"""

    def update_book(
        self, book_id: int, title: str, author: str, year: int, status: str
    ) -> None:

        try:
            book_id = int(book_id)
            year = int(year)
        except ValueError:
            print("Ошибка: ID и год должны быть числами!")
            return None

        found_book = [book for book in self.books if book["id"] == book_id]
        if not found_book:
            print(f"Книга с ID {book_id} не найдена!")
            return None

        book = found_book[0]
        book["title"] = title
        book["author"] = author
        book["year"] = year
        book["status"] = status
        print("Книга изменена успешно!")
        self.save_books()
