import sqlite3

class DB_Table:
    def __init__(self, db_name: str) -> None:
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS guest(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_address TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS administrator(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_address TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS image(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                high_res_img_fname TEXT UNIQUE,
                low_res_img_fname TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS request(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guest_id INTEGER,
                img_id INTEGER,
                reason TEXT,
                status INTEGER
            );
        """)
        self.conn.commit()

    def set_table_name(self, table_name) -> None:
        self.table_name = table_name

    def insert(self, data: dict) -> bool:
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            sql = f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})"
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
            return False

    def delete(self, criteria: dict) -> bool:
        try:
            where_clause = ' AND '.join([f"{key} = ?" for key in criteria])
            sql = f"DELETE FROM {self.table_name} WHERE {where_clause}"
            self.cur.execute(sql, list(criteria.values()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return False

    def read(self, criteria: dict = None, limit: int = None, offset: int = None) -> list:
        try:
            where_clause = ' AND '.join([f"{key} = ?" for key in criteria]) if criteria else ""
            limit_clause = f"LIMIT {limit}" if limit else ""
            offset_clause = f"OFFSET {offset}" if offset else ""
            sql = f"SELECT * FROM {self.table_name} " + \
                  (f"WHERE {where_clause} " if where_clause else "") + \
                  (f"{limit_clause} " if limit_clause else "") + \
                  (f"{offset_clause}" if offset_clause else "")
            self.cur.execute(sql, list(criteria.values()) if criteria else [])
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return []

    def read_range(self, min_id: int, max_id: int) -> list:
        try:
            sql = f"SELECT * FROM {self.table_name} WHERE id BETWEEN ? AND ?"
            self.cur.execute(sql, (min_id, max_id))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return []

    def update(self, data: dict, criteria: dict) -> bool:
        try:
            set_clause = ', '.join([f"{key} = ?" for key in data])
            where_clause = ' AND '.join([f"{key} = ?" for key in criteria])
            sql = f"UPDATE {self.table_name} SET {set_clause} WHERE {where_clause}"
            self.cur.execute(sql, list(data.values()) + list(criteria.values()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            return False

    def __del__(self):
        self.conn.close()

"""
# Example usage:
db = DB_Table('images_hub.db')
db.set_table_name('guest')
# db.insert({'email_address': 'shlabisa@sarao.ac.za'})
print(db.read())
# db.update({'email_address': 'new@example.com'}, {'email_address': 'shlabisa@sarao.ac.za'})
db.delete({'email_address': 'new@example.com'})
"""
