import sqlite3

def create_database():
    conn = sqlite3.connect('bookstore.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            price REAL
        )
    ''')

    books = [
        ("Think Python", "Allen B. Downey", 475.0),
        ("Automate the Boring Stuff with Python", "Al Sweigart", 599.0),
        ("Fluent Python", "Luciano Ramalho", 799.0)
    ]
    cursor.executemany("INSERT INTO books (title, author, price) VALUES (?, ?, ?)", books)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
import sqlite3

def fetch_price(title):
    conn = sqlite3.connect('bookstore.db')
    cursor = conn.cursor()

    cursor.execute("SELECT price FROM books WHERE title = ?", (title,))
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else None

def main():
    title = input("Enter the book title: ")
    quantity = int(input("Enter the quantity: "))

    price = fetch_price(title)
    if price:
        total_amount = price * quantity
        print(f"Total amount: Rs. {total_amount}")
    else:
        print("Book not found in the database.")

if __name__ == "__main__":
    main()
