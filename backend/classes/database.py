import os
from dotenv import load_dotenv
import sqlite3

class Database:
    def __init__(self) -> None:
        load_dotenv()
        env = os.getenv('FLASK_ENV', 'development')

        self.name = f"databases/{env}.db"
        self.conn = sqlite3.connect(self.name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS user(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `email_address` TEXT UNIQUE,
                `type` INTEGER
            );

            CREATE TABLE IF NOT EXISTS image(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `high_res_img_fname` TEXT UNIQUE,
                `low_res_img_fname` TEXT UNIQUE,
                `metadata` TEXT
            );

            CREATE TABLE IF NOT EXISTS request(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `user_id` INTEGER,
                `image_id` INTEGER,
                `reason` TEXT,
                `status` INTEGER
            );

            CREATE TABLE IF NOT EXISTS link(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `image_id` INTEGER,
                `key` TEXT,
                `limit` INTEGER
            );
        """)
        self.conn.commit()

    def insert(self, table_name: str, data: dict) -> bool:
        try:
            columns = ', '.join([f"`{key}`" for key in data.keys()])
            placeholders = ', '.join(['?' for _ in data])
            sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
            return False

    def delete(self, table_name: str, criteria: dict) -> bool:
        try:
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria])
            sql = f"DELETE FROM `{table_name}` WHERE {where_clause}"
            self.cur.execute(sql, list(criteria.values()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return False

    def read(self, table_name: str, criteria: dict = None, limit: int = None, offset: int = None) -> list:
        try:
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria]) if criteria else ""
            limit_clause = f"LIMIT {limit}" if limit else ""
            offset_clause = f"OFFSET {offset}" if offset else ""
            sql = f"SELECT * FROM `{table_name}` " + \
                  (f"WHERE {where_clause} " if where_clause else "") + \
                  (f"{limit_clause} " if limit_clause else "") + \
                  (f"{offset_clause}" if offset_clause else "")
            self.cur.execute(sql, list(criteria.values()) if criteria else [])
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return []

    def read_range(self, table_name: str, min_id: int, max_id: int) -> list:
        try:
            sql = f"SELECT * FROM `{table_name}` WHERE `id` BETWEEN ? AND ?"
            self.cur.execute(sql, (min_id, max_id))
            return self.cur.fetchall()
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return []

    def update(self, table_name: str, data: dict, criteria: dict) -> bool:
        try:
            set_clause = ', '.join([f"`{key}` = ?" for key in data])
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria])
            sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {where_clause}"
            print(sql)
            self.cur.execute(sql, list(data.values()) + list(criteria.values()))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            return False

    def clear(self) -> bool:
        if 'production' not in self.name:
            try:
                # Drop all tables
                self.cur.executescript("""
                    DROP TABLE IF EXISTS `user`;
                    DROP TABLE IF EXISTS `administrator`;
                    DROP TABLE IF EXISTS `image`;
                    DROP TABLE IF EXISTS `request`;
                    DROP TABLE IF EXISTS `link`;
                """)
                self.conn.commit()
                # Recreate tables
                self.create_tables()
                return True
            except sqlite3.Error as e:
                print(f"Error clearing the database: {e}")
                return False
        return False



    def __del__(self):
        self.conn.close()

"""
# Example usage:
db = Database()
# db.insert('user', {'email_address': 'shlabisa@sarao.ac.za'})
print(db.read('user'))
# db.update('user', {'email_address': 'new@example.com'}, {'email_address': 'shlabisa@sarao.ac.za'})
db.delete('user', {'email_address': 'new@example.com'})
"""
