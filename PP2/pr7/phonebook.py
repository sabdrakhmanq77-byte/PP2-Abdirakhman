import psycopg2
from psycopg2 import sql
import csv

# --- DATABASE SETUP ---
def setup_database():
    """Initializes the database and creates the contacts table."""
    conn = psycopg2.connect(
        host="localhost",
        database="suppliers",
        user="postgres",
        password="LIBRA0237"
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
          name VARCHAR(100),
          phone VARCHAR(20) UNIQUE
        )
    ''')
    conn.commit()
    return conn

# --- FUNCTIONS ---

def insert_from_csv(conn, file_path):
    """Imports contacts from a CSV file (Name, Phone)."""
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            cursor = conn.cursor()
            count = 0
            for row in csv.reader(f):
                if len(row) >= 2:
                    cursor.execute(
                        "INSERT INTO contacts (name, phone) VALUES (%s, %s) ON CONFLICT (phone) DO NOTHING",
                        (row[0].strip(), row[1].strip())
                    )
                    if cursor.rowcount:
                        count += 1
            conn.commit()
            print(f"Imported {count} contacts.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

def insert_from_console(conn):
    """Adds a single contact via manual entry."""
    name = input("Enter Name: ").strip()
    phone = input("Enter Phone: ").strip()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
        conn.commit()
        print("Contact added.")
    except psycopg2.IntegrityError:
        conn.rollback()
        print("Error: Duplicate phone number.")

def update_contact(conn):
    """Updates contact information based on phone number."""
    current_phone = input("Enter current phone to update: ").strip()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE phone = %s", (current_phone,))
    contact = cursor.fetchone()
    if not contact:
        print("Contact not found.")
        return
    
    print("1. Update Name\n2. Update Phone")
    choice = input("Select option: ")
    if choice == '1':
        new_val = input("Enter new name: ").strip()
        cursor.execute("UPDATE contacts SET name = %s WHERE phone = %s", (new_val, current_phone))
    elif choice == '2':
        new_val = input("Enter new phone: ").strip()
        try:
            cursor.execute("UPDATE contacts SET phone = %s WHERE phone = %s", (new_val, current_phone))
        except psycopg2.IntegrityError:
            conn.rollback()
            print("Error: Number already exists.")
            return
    conn.commit()
    print("Updated successfully.")

def query_contacts(conn):
    """Searches by name (partial) or phone prefix."""
    print("1. Search Name\n2. Search Phone")
    choice = input("Select option: ")
    term = input("Enter search term: ").strip()
    cursor = conn.cursor()
    if choice == '1':
        cursor.execute("SELECT * FROM contacts WHERE name LIKE %s", (f'%{term}%',))
    else:
        cursor.execute("SELECT * FROM contacts WHERE phone LIKE %s", (f'{term}%',))
    for row in cursor.fetchall():
        print(f"Name: {row[0]} | Phone: {row[1]}")

def delete_contact(conn):
    """Deletes a contact by name or phone."""
    target = input("Enter Name or Phone to delete: ").strip()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE name = %s OR phone = %s", (target, target))
    conn.commit()
    print(f"Deleted {cursor.rowcount} row(s).")

def show_contacts(conn):
    """Displays all contacts in the table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    if not rows:
        print("No contacts found.")
    else:
        print("All Contacts:")
        for row in rows:
            print(f"Name: {row[0]} | Phone: {row[1]}")

# --- MAIN MENU ---
def main():
    conn = setup_database()
    while True:
        print("\n--- MENU ---\n1. CSV Import\n2. Add\n3. Update\n4. Search\n5. Delete\n6. Show All\n7. Exit")
        choice = input("Option: ")
        if choice == '1': insert_from_csv(conn, input("CSV Path: "))
        elif choice == '2': insert_from_console(conn)
        elif choice == '3': update_contact(conn)
        elif choice == '4': query_contacts(conn)
        elif choice == '5': delete_contact(conn)
        elif choice == '6': show_contacts(conn)
        elif choice == '7': break
    conn.close()

if __name__ == "__main__":
    main()
