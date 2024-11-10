import sqlite3
conn = sqlite3.connect('crm.db')
cursor = conn.cursor()
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            date TEXT NOT NULL,
            interaction_type TEXT,
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            FOREIGN KEY (customer_id) REFERENCES Customers(id)
        )
    ''')
    conn.commit()
def add_customer(name, email, phone, address):
    cursor.execute('''
        INSERT INTO Customers (name, email, phone, address)
        VALUES (?, ?, ?, ?)
    ''', (name, email, phone, address))
    conn.commit()
    print("Customer added successfully.")
def log_interaction(customer_id, date, interaction_type, notes):
    cursor.execute('''
        INSERT INTO Interactions (customer_id, date, interaction_type, notes)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, date, interaction_type, notes))
    conn.commit()
    print("Interaction logged successfully.")
def log_sale(customer_id, date, amount, description):
    cursor.execute('''
        INSERT INTO Sales (customer_id, date, amount, description)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, date, amount, description))
    conn.commit()
    print("Sale logged successfully.")

def get_customer_details(customer_id):
    cursor.execute('SELECT * FROM Customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    
    if customer:
        print("Customer Details:")
        print("ID:", customer[0])
        print("Name:", customer[1])
        print("Email:", customer[2])
        print("Phone:", customer[3])
        print("Address:", customer[4])

        print("\nInteractions:")
        cursor.execute('SELECT * FROM Interactions WHERE customer_id = ?', (customer_id,))
        interactions = cursor.fetchall()
        for interaction in interactions:
            print(interaction)

        print("\nSales:")
        cursor.execute('SELECT * FROM Sales WHERE customer_id = ?', (customer_id,))
        sales = cursor.fetchall()
        for sale in sales:
            print(sale)
    else:
        print("Customer not found.")
create_tables()
add_customer('Roy', 'roy14@gmail.com', '123-456-7890', '123 Delhi')
log_interaction(1, '2023-10-01', 'Phone Call', 'Discussed product updates')
log_sale(1, '2023-10-02', 500, 'Purchased software license')
get_customer_details(1)
conn.close()
