import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('contacts.db')
cursor = conn.cursor()

# Create table for contacts
def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT
        )
    ''')
    conn.commit()

# Function to add a new contact
def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    email = input("Enter email (optional): ")
    address = input("Enter address (optional): ")
    
    cursor.execute('''
        INSERT INTO Contacts (name, phone, email, address)
        VALUES (?, ?, ?, ?)
    ''', (name, phone, email if email else None, address if address else None))
    conn.commit()
    print("Contact added successfully.")

# Function to update an existing contact
def update_contact():
    contact_id = input("Enter contact ID to update: ")
    cursor.execute('SELECT * FROM Contacts WHERE id = ?', (contact_id,))
    contact = cursor.fetchone()
    
    if not contact:
        print("Contact not found.")
        return
    
    name = input(f"Enter new name (leave blank to keep '{contact[1]}'): ") or contact[1]
    phone = input(f"Enter new phone (leave blank to keep '{contact[2]}'): ") or contact[2]
    email = input(f"Enter new email (leave blank to keep '{contact[3]}'): ") or contact[3]
    address = input(f"Enter new address (leave blank to keep '{contact[4]}'): ") or contact[4]
    
    cursor.execute('''
        UPDATE Contacts SET name = ?, phone = ?, email = ?, address = ?
        WHERE id = ?
    ''', (name, phone, email, address, contact_id))
    conn.commit()
    print("Contact updated successfully.")

# Function to delete a contact
def delete_contact():
    contact_id = input("Enter contact ID to delete: ")
    cursor.execute('DELETE FROM Contacts WHERE id = ?', (contact_id,))
    conn.commit()
    print("Contact deleted successfully.")

# Function to search for contacts
def search_contacts():
    search_term = input("Enter search term: ")
    cursor.execute('''
        SELECT * FROM Contacts 
        WHERE name LIKE ? OR phone LIKE ? OR email LIKE ? OR address LIKE ?
    ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    contacts = cursor.fetchall()
    
    if contacts:
        print("Search Results:")
        for contact in contacts:
            print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}, Address: {contact[4]}")
    else:
        print("No contacts found.")

# Function to list all contacts
def list_contacts():
    cursor.execute('SELECT * FROM Contacts')
    contacts = cursor.fetchall()
    
    print("All Contacts:")
    for contact in contacts:
        print(f"ID: {contact[0]}, Name: {contact[1]}, Phone: {contact[2]}, Email: {contact[3]}, Address: {contact[4]}")

# Main menu
def main_menu():
    while True:
        print("\nContact Management System")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. Search Contacts")
        print("5. List All Contacts")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_contact()
        elif choice == '2':
            update_contact()
        elif choice == '3':
            delete_contact()
        elif choice == '4':
            search_contacts()
        elif choice == '5':
            list_contacts()
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Setup database and table, and run the main menu
create_table()
main_menu()

# Close the database connection
conn.close()
