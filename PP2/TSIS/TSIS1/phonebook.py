import csv
import json                         
from datetime import date            #For birthdays
from connect import get_connection

def create_tables():
    """Создаёт все таблицы и процедуры из .sql файлов."""
    try:
        conn = get_connection()
        if conn is None:
            return
        cur = conn.cursor()

        #all procedures and functions
        for fname in ('schema.sql', 'procedures.sql'):
            with open(fname, encoding='utf-8') as f:
                cur.execute(f.read())

        conn.commit()
        print('Tables and procedures are ready.')
    except Exception as e:
        print(f'Error creating tables: {e}')
    finally:
        cur.close()
        conn.close()


def insert_console():
    name     = input('Name: ').strip()
    email    = input('Email (Enter to skip): ').strip() or None
    birthday = input('Birthday YYYY-MM-DD (Enter to skip): ').strip() or None
    group    = input('Group (Family/Work/Friend/Other, Enter to skip): ').strip() or None

    try:
        conn = get_connection()
        cur  = conn.cursor()

        #Getting group id
        group_id = _get_or_create_group(cur, group) if group else None

        #Inserting
        cur.execute(
            '''INSERT INTO contacts (name, email, birthday, group_id)
               VALUES (%s, %s, %s, %s)
               ON CONFLICT (name) DO NOTHING
               RETURNING id;''',
            (name, email, birthday, group_id)
        )
        row = cur.fetchone()
        if row is None:
            print('Contact with this name already exists.')
            return
        contact_id = row[0]

        #Adding one or more phones
        _add_phones_interactive(cur, contact_id)

        conn.commit()
        print('Contact saved.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def _add_phones_interactive(cur, contact_id):
    """Asking numbers"""
    print('Add phone numbers (Enter empty phone to stop):')
    while True:
        phone = input('  Phone: ').strip()
        if not phone:
            break
        ptype = input('  Type (home/work/mobile): ').strip()
        if ptype not in ('home', 'work', 'mobile'):
            print('  Invalid type, defaulting to mobile.')
            ptype = 'mobile'
        cur.execute(
            'INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);',
            (contact_id, phone, ptype)
        )


def _get_or_create_group(cur, group_name: str) -> int:
    """Returns group id, creates if not exists"""
    cur.execute('SELECT id FROM groups WHERE name = %s;', (group_name,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute('INSERT INTO groups (name) VALUES (%s) RETURNING id;', (group_name,))
    return cur.fetchone()[0]


#CSV: name, phone, phone_type, email, birthday, group
def insert_csv(filepath: str):
    try:
        conn = get_connection()
        cur  = conn.cursor()

        with open(filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)   
            for row in reader:
                name     = row.get('name', '').strip()
                phone    = row.get('phone', '').strip()
                ptype    = row.get('phone_type', 'mobile').strip()
                email    = row.get('email', '').strip() or None
                birthday = row.get('birthday', '').strip() or None
                group    = row.get('group', '').strip() or None

                if not name:
                    continue

                group_id = _get_or_create_group(cur, group) if group else None

                cur.execute(
                    '''INSERT INTO contacts (name, email, birthday, group_id)
                       VALUES (%s, %s, %s, %s)
                       ON CONFLICT (name) DO NOTHING
                       RETURNING id;''',
                    (name, email, birthday, group_id)
                )
                result = cur.fetchone()
                if result and phone:
                    cur.execute(
                        'INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);',
                        (result[0], phone, ptype)
                    )

        conn.commit()
        print('CSV imported successfully.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()



def export_json(filepath: str = 'contacts.json'):
    """Exports to json contacts with telephones and group"""
    try:
        conn = get_connection()
        cur  = conn.cursor()

        cur.execute('''
            SELECT c.id, c.name, c.email, c.birthday, g.name AS grp
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.name;
        ''')
        contacts = cur.fetchall()

        result = []
        for c in contacts:
            cid, name, email, birthday, grp = c
            cur.execute('SELECT phone, type FROM phones WHERE contact_id = %s;', (cid,))
            phones = [{'phone': p[0], 'type': p[1]} for p in cur.fetchall()]

            result.append({
                'name':     name,
                'email':    email,
                'birthday': birthday.isoformat() if isinstance(birthday, date) else birthday,
                'group':    grp,
                'phones':   phones
            })

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f'Exported {len(result)} contacts to {filepath}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()

def import_json(filepath: str = 'contacts.json'):
    """Reads json, writing data. If name exists - asking"""
    try:
        conn = get_connection()
        cur  = conn.cursor()

        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)

        for c in data:
            name     = c.get('name', '').strip()
            email    = c.get('email')
            birthday = c.get('birthday')
            group    = c.get('group')
            phones   = c.get('phones', [])

            if not name:
                continue

            #Copy check
            cur.execute('SELECT id FROM contacts WHERE name = %s;', (name,))
            existing = cur.fetchone()

            if existing:
                choice = input(f'"{name}" already exists. Overwrite? (y/n): ').strip().lower()
                if choice != 'y':
                    print(f'  Skipped "{name}"')
                    continue
                #Rewriting
                group_id = _get_or_create_group(cur, group) if group else None
                cur.execute(
                    '''UPDATE contacts SET email=%s, birthday=%s, group_id=%s WHERE name=%s;''',
                    (email, birthday, group_id, name)
                )
                cur.execute('DELETE FROM phones WHERE contact_id=%s;', (existing[0],))
                contact_id = existing[0]
            else:
                group_id = _get_or_create_group(cur, group) if group else None
                cur.execute(
                    '''INSERT INTO contacts (name, email, birthday, group_id)
                       VALUES (%s, %s, %s, %s) RETURNING id;''',
                    (name, email, birthday, group_id)
                )
                contact_id = cur.fetchone()[0]

            #Inserting
            for p in phones:
                cur.execute(
                    'INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s);',
                    (contact_id, p.get('phone'), p.get('type', 'mobile'))
                )

        conn.commit()
        print('JSON import complete.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def update_name_by_num(number, new_name):
    sql = '''UPDATE contacts SET name = %s
             WHERE id = (SELECT contact_id FROM phones WHERE phone = %s LIMIT 1);'''
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(sql, (new_name, number))
        conn.commit()
        print('Name updated.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def update_num_by_name(name, new_number):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute('SELECT id FROM contacts WHERE name = %s;', (name,))
        row = cur.fetchone()
        if not row:
            print('Contact not found.')
            return
        cur.execute(
            'UPDATE phones SET phone = %s WHERE contact_id = %s AND id = (SELECT MIN(id) FROM phones WHERE contact_id = %s);',
            (new_number, row[0], row[0])
        )
        conn.commit()
        print('Phone updated.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def update():
    print('1. Update name by phone number')
    print('2. Update phone number by name')
    n = input('1/2: ')
    if n == '1':
        number   = input('Phone number: ')
        new_name = input('New name: ')
        update_name_by_num(number, new_name)
    elif n == '2':
        name       = input('Name: ')
        new_number = input('New phone number: ')
        update_num_by_name(name, new_number)
    else:
        print('Incorrect.')

def search_menu():
    print('\n--- Search & Filter ---')
    print('1. Search by name / email / phone  (uses search_contacts function)')
    print('2. Filter by group')
    print('3. Search by email')
    print('4. Paginated list (all contacts)')
    n = input('Choose: ')

    if n == '1':
        q = input('Search query: ')
        _run_search_function(q)
    elif n == '2':
        _filter_by_group()
    elif n == '3':
        _search_by_email()
    elif n == '4':
        _paginated_list()
    else:
        print('Incorrect.')


def _run_search_function(query: str):
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute('SELECT * FROM search_contacts(%s);', (query,))
        rows = cur.fetchall()
        if not rows:
            print('Nothing found.')
        for r in rows:
            print(f'  [{r[0]}] {r[1]} | email: {r[2]} | birthday: {r[3]} | group: {r[4]}')
            cur.execute('SELECT phone, type FROM phones WHERE contact_id = %s;', (r[0],))
            for p in cur.fetchall():
                print(f'{p[0]} ({p[1]})')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def _filter_by_group():
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute('SELECT id, name FROM groups ORDER BY name;')
        groups = cur.fetchall()
        print('Available groups:')
        for g in groups:
            print(f'  {g[0]}. {g[1]}')
        gid = input('Enter group id: ').strip()

        print('Sort by: 1-name  2-birthday  3-date added')
        s = input('Sort: ')
        order = {'1': 'c.name', '2': 'c.birthday', '3': 'c.created_at'}.get(s, 'c.name')

        cur.execute(f'''
            SELECT c.id, c.name, c.email, c.birthday
            FROM contacts c
            WHERE c.group_id = %s
            ORDER BY {order};
        ''', (gid,))
        rows = cur.fetchall()
        if not rows:
            print('No contacts in this group.')
        for r in rows:
            print(f'  [{r[0]}] {r[1]} | {r[2]} | {r[3]}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def _search_by_email():
    q = input('Email search query: ').strip()
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute(
            'SELECT id, name, email, birthday FROM contacts WHERE email ILIKE %s;',
            (f'%{q}%',)
        )
        rows = cur.fetchall()
        if not rows:
            print('Nothing found.')
        for r in rows:
            print(f'  [{r[0]}] {r[1]} | {r[2]} | {r[3]}')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def _paginated_list():
    page_size = 5
    offset    = 0

    try:
        conn = get_connection()
        cur  = conn.cursor()

        while True:
            cur.execute(
                '''SELECT c.name, c.email, g.name
                   FROM contacts c
                   LEFT JOIN groups g ON g.id = c.group_id
                   ORDER BY c.name
                   LIMIT %s OFFSET %s;''',
                (page_size, offset)
            )
            rows = cur.fetchall()

            if not rows:
                print('No more contacts.')
                break

            print(f'\n--- Page (offset={offset}) ---')
            for r in rows:
                print(f'  {r[0]} | {r[1]} | group: {r[2]}')

            cmd = input('next / prev / quit: ').strip().lower()
            if cmd == 'next':
                offset += page_size
            elif cmd == 'prev':
                offset = max(0, offset - page_size)
            elif cmd == 'quit':
                break
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def delete():
    n = input('Delete by name (1) or by phone number (2): ')
    try:
        conn = get_connection()
        cur  = conn.cursor()
        if n == '1':
            name = input('Name: ')
            cur.execute('DELETE FROM contacts WHERE name = %s;', (name,))
            print('Contact deleted.')
        elif n == '2':
            num = input('Phone number: ')
            cur.execute(
                'DELETE FROM contacts WHERE id = (SELECT contact_id FROM phones WHERE phone = %s LIMIT 1);',
                (num,)
            )
            print('Contact deleted.')
        else:
            print('Incorrect choice.')
            return
        conn.commit()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def call_add_phone():
    name  = input('Contact name: ').strip()
    phone = input('Phone: ').strip()
    ptype = input('Type (home/work/mobile): ').strip()
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute('CALL add_phone(%s, %s, %s);', (name, phone, ptype))
        conn.commit()
        print('Done.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()


def call_move_to_group():
    name  = input('Contact name: ').strip()
    group = input('Target group: ').strip()
    try:
        conn = get_connection()
        cur  = conn.cursor()
        cur.execute('CALL move_to_group(%s, %s);', (name, group))
        conn.commit()
        print('Done.')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        cur.close(); conn.close()



def main():
    create_tables()
    print('\n' + '=' * 45)
    print('Welcome to PhoneBook TSIS 1!')

    while True:
        print('=' * 45)
        print('1.  Insert from console')
        print('2.  Insert from CSV')
        print('3.  Update info')
        print('4.  Search & Filter')          
        print('5.  Delete info')
        print('6.  Export to JSON')           
        print('7.  Import from JSON')         
        print('8.  Add phone to contact')     
        print('9.  Move contact to group')   
        print('0.  Exit')
        print('=' * 45)

        n = input('Action: ')

        if   n == '1': insert_console()
        elif n == '2': insert_csv(r'C:\git_practice\TSIS\database\contacts.csv')
        elif n == '3': update()
        elif n == '4': search_menu()
        elif n == '5': delete()
        elif n == '6': export_json()
        elif n == '7': import_json()
        elif n == '8': call_add_phone()
        elif n == '9': call_move_to_group()
        elif n == '0': print('Goodbye!'); break
        else:          print('Incorrect. Try again.')

if __name__ == '__main__':
    main()