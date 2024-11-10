import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# Create tables for users and tasks
def create_tables():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            assigned_user INTEGER,
            due_date TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (assigned_user) REFERENCES Users(id)
        )
    ''')
    conn.commit()

# Function to add a new user
def add_user():
    name = input("Enter user name: ")
    cursor.execute('INSERT INTO Users (name) VALUES (?)', (name,))
    conn.commit()
    print("User added successfully.")

# Function to add a new task
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")
    
    cursor.execute('''
        INSERT INTO Tasks (title, description, due_date)
        VALUES (?, ?, ?)
    ''', (title, description, due_date))
    conn.commit()
    print("Task added successfully.")

# Function to assign a task to a user
def assign_task():
    task_id = input("Enter task ID to assign: ")
    user_id = input("Enter user ID to assign to: ")

    cursor.execute('SELECT * FROM Tasks WHERE id = ?', (task_id,))
    if cursor.fetchone() is None:
        print("Task not found.")
        return

    cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
    if cursor.fetchone() is None:
        print("User not found.")
        return

    cursor.execute('UPDATE Tasks SET assigned_user = ? WHERE id = ?', (user_id, task_id))
    conn.commit()
    print("Task assigned successfully.")

# Function to update the status of a task
def update_task_status():
    task_id = input("Enter task ID to update: ")
    new_status = input("Enter new status (Pending, In Progress, Completed): ")

    if new_status not in ["Pending", "In Progress", "Completed"]:
        print("Invalid status.")
        return

    cursor.execute('SELECT * FROM Tasks WHERE id = ?', (task_id,))
    if cursor.fetchone() is None:
        print("Task not found.")
        return

    cursor.execute('UPDATE Tasks SET status = ? WHERE id = ?', (new_status, task_id))
    conn.commit()
    print("Task status updated successfully.")

# Function to view tasks by status or assigned user
def view_tasks():
    filter_type = input("Filter tasks by (status/user): ").lower()
    
    if filter_type == "status":
        status = input("Enter status (Pending, In Progress, Completed): ")
        cursor.execute('SELECT * FROM Tasks WHERE status = ?', (status,))
    elif filter_type == "user":
        user_id = input("Enter user ID: ")
        cursor.execute('SELECT * FROM Tasks WHERE assigned_user = ?', (user_id,))
    else:
        print("Invalid filter type.")
        return
    
    tasks = cursor.fetchall()
    if tasks:
        print("\nTasks:")
        for task in tasks:
            assigned_user = task[3] if task[3] else "Unassigned"
            print(f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Assigned User: {assigned_user}, Due Date: {task[4]}, Status: {task[5]}")
    else:
        print("No tasks found.")

# Function to list all users
def list_users():
    cursor.execute('SELECT * FROM Users')
    users = cursor.fetchall()
    
    print("\nUsers:")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}")

# Main menu
def main_menu():
    while True:
        print("\nTask Assignment and Tracking System")
        print("1. Add User")
        print("2. Add Task")
        print("3. Assign Task")
        print("4. Update Task Status")
        print("5. View Tasks")
        print("6. List Users")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_user()
        elif choice == '2':
            add_task()
        elif choice == '3':
            assign_task()
        elif choice == '4':
            update_task_status()
        elif choice == '5':
            view_tasks()
        elif choice == '6':
            list_users()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Setup database and tables, and run the main menu
create_tables()
main_menu()

# Close the database connection
conn.close()
