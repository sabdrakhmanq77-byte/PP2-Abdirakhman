from connect import get_connection

def apply_sql_file(filename):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            with open(filename, 'r', encoding='utf-8') as f:
                cur.execute(f.read())
            conn.commit()
            print(f"✅ Скрипт {filename} успешно применен!")
            cur.close()
        except Exception as e:
            print(f"❌ Ошибка в файле {filename}: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    apply_sql_file('functions.sql')
    apply_sql_file('procedures.sql')
    