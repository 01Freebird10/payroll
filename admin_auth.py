import hashlib
from datetime import datetime


class AdminAuth:
    def __init__(self, db):
        self.db = db

    def authenticate(self, username, password):
        query = "SELECT * FROM admins WHERE username = ? AND password = ?"
        result = self.db.execute_single("admin", query, (username, password))

        if result:
            update_query = "UPDATE admins SET last_login = ? WHERE username = ?"
            self.db.execute_update("admin", update_query, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), username))
            return True
        return False

    def add_admin(self, username, password):
        query = "INSERT INTO admins (username, password) VALUES (?, ?)"
        try:
            self.db.execute_update("admin", query, (username, password))
            return True
        except:
            return False

    def get_admins(self):
        query = "SELECT id, username, created_at, last_login FROM admins"
        return self.db.execute_query("admin", query)

    def update_admin_password(self, username, new_password):
        query = "UPDATE admins SET password = ? WHERE username = ?"
        rows_affected = self.db.execute_update("admin", query, (new_password, username))
        return rows_affected > 0

    def delete_admin(self, username):
        query = "DELETE FROM admins WHERE username = ?"
        rows_affected = self.db.execute_update("admin", query, (username,))
        return rows_affected > 0