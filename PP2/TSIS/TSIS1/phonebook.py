import json
from connect import get_connection

def add_contact():
    try:
        name = input("Name: ")
        email = input("Email: ")
        birthday = input("Birthday (YYYY-MM-DD): ")
        group = input("Group: ")

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT DO NOTHING", (group,))
        cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
        group_result = cur.fetchone()
        if group_result is None:
            print("Error: Group not found")
            return
        gid = group_result[0]

        cur.execute(
            "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s)",
            (name,email,birthday,gid)
        )

        conn.commit()
        print("Contact added successfully")
    except Exception as e:
        print(f"Error adding contact: {e}")
    finally:
        cur.close()
        conn.close()

def search():
    try:
        q = input("Search: ")
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        results = cur.fetchall()
        if not results:
            print("No results found")
        else:
            for row in results:
                print(row)
    except Exception as e:
        print(f"Error searching: {e}")
    finally:
        cur.close()
        conn.close()

def filter_group():
    try:
        g = input("Group: ")
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.name, c.email
            FROM contacts c
            JOIN groups g ON c.group_id = g.id
            WHERE g.name=%s
        """, (g,))

        results = cur.fetchall()
        if not results:
            print("No contacts in this group")
        else:
            print(results)
    except Exception as e:
        print(f"Error filtering by group: {e}")
    finally:
        cur.close()
        conn.close()

def export_json():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT c.id, c.name, c.email, c.birthday, g.name as group_name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id=g.id
        """)

        contacts = cur.fetchall()
        data = []
        
        for contact in contacts:
            contact_id, name, email, birthday, group = contact
            cur.execute("SELECT phone FROM phones WHERE contact_id=%s", (contact_id,))
            phones = [row[0] for row in cur.fetchall()]
            
            data.append({
                "name": name,
                "email": email,
                "birthday": birthday,
                "group": group,
                "phones": phones
            })

        with open("contacts.json","w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False, default=str)

        print(f"Exported {len(data)} contacts")
    except Exception as e:
        print(f"Error exporting: {e}")
    finally:
        cur.close()
        conn.close()

def import_json():
    try:
        with open("contacts.json") as f:
            data = json.load(f)

        conn = get_connection()
        cur = conn.cursor()
        imported_count = 0

        for item in data:
            if isinstance(item, dict):
                name = item.get("name")
                email = item.get("email")
                birthday = item.get("birthday")
                group = item.get("group")
                phones = item.get("phones", [])
            else:
                name, email, birthday, group, phone = item
                phones = [phone] if phone else []

            if not name:
                continue

            cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
            exists = cur.fetchone()

            if exists:
                ans = input(f"{name} exists. overwrite? y/n: ")
                if ans != "y":
                    continue
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

            cur.execute("INSERT INTO groups(name) VALUES(%s) ON CONFLICT DO NOTHING", (group,))
            cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
            group_result = cur.fetchone()
            gid = group_result[0] if group_result else None

            cur.execute(
                "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s) RETURNING id",
                (name, email, birthday, gid)
            )
            contact_result = cur.fetchone()
            if contact_result is None:
                continue
            cid = contact_result[0]

            for phone in phones:
                if phone:
                    cur.execute("INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,'mobile')", (cid, phone))

            imported_count += 1

        conn.commit()
        print(f"Imported {imported_count} contacts")
    except FileNotFoundError:
        print("Error: contacts.json file not found")
    except json.JSONDecodeError:
        print("Error: Invalid JSON file format")
    except Exception as e:
        print(f"Error importing: {e}")
    finally:
        cur.close()
        conn.close()

def menu():
    while True:
        try:
            print("""
1 Add
2 Search
3 Filter by group
4 Export JSON
5 Import JSON
0 Exit
        """)

            c = input("> ").strip()

            if c=="1": add_contact()
            elif c=="2": search()
            elif c=="3": filter_group()
            elif c=="4": export_json()
            elif c=="5": import_json()
            elif c=="0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

menu()