import sqlite3
import os
from datetime import datetime


class Database:
    def __init__(self):
        self.db_dir = "databases"
        self.ensure_database_directory()
        self.init_databases()

    def ensure_database_directory(self):
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

    def init_databases(self):
        self.init_admin_db()
        self.init_employee_db()
        self.init_salary_db()
        self.init_payroll_db()

    def init_admin_db(self):
        conn = sqlite3.connect(f"{self.db_dir}/admin.db")
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS admins
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           username
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           password
                           TEXT
                           NOT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           last_login
                           TIMESTAMP
                       )
                       ''')

        cursor.execute("SELECT * FROM admins WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO admins (username, password) VALUES (?, ?)",
                           ('admin', 'admin123'))

        conn.commit()
        conn.close()

    def init_employee_db(self):
        conn = sqlite3.connect(f"{self.db_dir}/employees.db")
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS employees
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           employee_id
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           first_name
                           TEXT
                           NOT
                           NULL,
                           last_name
                           TEXT
                           NOT
                           NULL,
                           email
                           TEXT
                           UNIQUE
                           NOT
                           NULL,
                           phone
                           TEXT,
                           department
                           TEXT
                           NOT
                           NULL,
                           position
                           TEXT
                           NOT
                           NULL,
                           hire_date
                           TEXT
                           NOT
                           NULL,
                           status
                           TEXT
                           DEFAULT
                           'active',
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       ''')

        conn.commit()
        conn.close()

    def init_salary_db(self):
        conn = sqlite3.connect(f"{self.db_dir}/salary.db")
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS salaries
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           employee_id
                           TEXT
                           NOT
                           NULL,
                           base_salary
                           REAL
                           NOT
                           NULL,
                           allowances
                           REAL
                           DEFAULT
                           0,
                           deductions
                           REAL
                           DEFAULT
                           0,
                           effective_date
                           TEXT
                           NOT
                           NULL,
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           FOREIGN
                           KEY
                       (
                           employee_id
                       ) REFERENCES employees
                       (
                           employee_id
                       )
                           )
                       ''')

        conn.commit()
        conn.close()

    def init_payroll_db(self):
        conn = sqlite3.connect(f"{self.db_dir}/payroll.db")
        cursor = conn.cursor()

        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS payroll_records
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           employee_id
                           TEXT
                           NOT
                           NULL,
                           period
                           TEXT
                           NOT
                           NULL,
                           base_salary
                           REAL
                           NOT
                           NULL,
                           allowances
                           REAL
                           DEFAULT
                           0,
                           deductions
                           REAL
                           DEFAULT
                           0,
                           net_salary
                           REAL
                           NOT
                           NULL,
                           payment_date
                           TEXT
                           DEFAULT
                           CURRENT_TIMESTAMP,
                           status
                           TEXT
                           DEFAULT
                           'processed',
                           created_at
                           TIMESTAMP
                           DEFAULT
                           CURRENT_TIMESTAMP
                       )
                       ''')

        conn.commit()
        conn.close()

    def get_connection(self, db_name):
        return sqlite3.connect(f"{self.db_dir}/{db_name}.db")

    def execute_query(self, db_name, query, params=()):
        conn = self.get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        result = cursor.fetchall()
        conn.close()
        return result

    def execute_update(self, db_name, query, params=()):
        conn = self.get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id

    def execute_single(self, db_name, query, params=()):
        conn = self.get_connection(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result