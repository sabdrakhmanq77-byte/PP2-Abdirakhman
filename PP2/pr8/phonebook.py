import psycopg2
from config import DB_CONFIG
from connect import get_connection

def upsert_contact(name, phone):
    """Задача 2: Процедура добавления или обновления контакта"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
            conn.commit()
            print(f"Контакт '{name}' обработан (добавлен/обновлен).")
            cur.close()
        except Exception as e:
            print(f"Ошибка upsert: {e}")
        finally:
            conn.close()

def search_contacts(pattern):
    """Задача 1: Поиск по паттерну (имя или телефон)"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
            rows = cur.fetchall()
            if rows:
                print(f"\nНайдено контактов по запросу '{pattern}':")
                for row in rows:
                    print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
            else:
                print("Ничего не найдено.")
            cur.close()
        finally:
            conn.close()

def bulk_insert_contacts():
    """Задача 3: Массовая вставка с валидацией телефона"""
    conn = get_connection()
    if conn:
        try:
            n = int(input("Сколько контактов добавить? "))
            names = []
            phones = []
            for i in range(n):
                name = input(f"  Имя {i+1}: ")
                phone = input(f"  Телефон {i+1}: ")
                names.append(name)
                phones.append(phone)

            cur = conn.cursor()
            cur.execute("SELECT * FROM bulk_insert_contacts(%s, %s)", (names, phones))
            bad_rows = cur.fetchall()
            conn.commit()

            if bad_rows:
                print("\nНекорректные данные (не добавлены):")
                for row in bad_rows:
                    print(f"  Имя: {row[0]} | Телефон: {row[1]}")
            else:
                print("Все контакты успешно добавлены.")
            cur.close()
        except Exception as e:
            print(f"Ошибка bulk insert: {e}")
        finally:
            conn.close()

def get_paginated_contacts(limit, offset):
    """Задача 4: Пагинация (LIMIT и OFFSET)"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            print(f"\nКонтакты (Лимит: {limit}, Смещение: {offset}):")
            for row in rows:
                print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")
            cur.close()
        finally:
            conn.close()

def delete_contact_proc(identifier):
    """Задача 5: Удаление по имени или номеру телефона"""
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("CALL delete_contact_by_name_or_phone(%s)", (identifier,))
            conn.commit()
            print(f"Запрос на удаление '{identifier}' выполнен.")
            cur.close()
        finally:
            conn.close()

if __name__ == "__main__":
    while True:
        print("\n--- PhoneBook (Practice 08: Functions & Procedures) ---")
        print("1. Добавить/Обновить контакт (Upsert)")
        print("2. Поиск по шаблону (Pattern Search)")
        print("3. Массовое добавление (Bulk Insert)")
        print("4. Показать страницу контактов (Pagination)")
        print("5. Удалить контакт (Delete)")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")

        if choice == '1':
            n = input("Введите имя: ")
            p = input("Введите телефон: ")
            upsert_contact(n, p)
        elif choice == '2':
            patt = input("Введите часть имени или номера: ")
            search_contacts(patt)
        elif choice == '3':
            bulk_insert_contacts()
        elif choice == '4':
            lim = int(input("Сколько записей показать? (Limit): "))
            off = int(input("Сколько пропустить? (Offset): "))
            get_paginated_contacts(lim, off)
        elif choice == '5':
            val = input("Введите имя или номер для удаления: ")
            delete_contact_proc(val)
        elif choice == '6':
            print("Выход...")
            break
        else:
            print("Неверный выбор.")