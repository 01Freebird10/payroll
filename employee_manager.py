import uuid
from datetime import datetime


class EmployeeManager:
    def __init__(self, db):
        self.db = db

    def add_employee(self, employee_data):
        employee_id = str(uuid.uuid4())[:8]

        query = '''
                INSERT INTO employees (employee_id, first_name, last_name, email, phone,
                                       department, position, hire_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) \
                '''

        try:
            self.db.execute_update("employees", query, (
                employee_id,
                employee_data['first_name'],
                employee_data['last_name'],
                employee_data['email'],
                employee_data['phone'],
                employee_data['department'],
                employee_data['position'],
                employee_data['hire_date'],
                employee_data['status']
            ))
            return True
        except:
            return False

    def get_all_employees(self):
        query = "SELECT * FROM employees ORDER BY last_name, first_name"
        results = self.db.execute_query("employees", query)

        employees = []
        for row in results:
            employees.append({
                'id': row[0],
                'employee_id': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'email': row[4],
                'phone': row[5],
                'department': row[6],
                'position': row[7],
                'hire_date': row[8],
                'status': row[9],
                'created_at': row[10]
            })
        return employees

    def get_employee_by_id(self, employee_id):
        query = "SELECT * FROM employees WHERE employee_id = ?"
        result = self.db.execute_single("employees", query, (employee_id,))

        if result:
            return {
                'id': result[0],
                'employee_id': result[1],
                'first_name': result[2],
                'last_name': result[3],
                'email': result[4],
                'phone': result[5],
                'department': result[6],
                'position': result[7],
                'hire_date': result[8],
                'status': result[9],
                'created_at': result[10]
            }
        return None

    def search_employee(self, search_term):
        query = '''
                SELECT * \
                FROM employees
                WHERE employee_id LIKE ? \
                   OR first_name LIKE ? \
                   OR last_name LIKE ?
                   OR email LIKE ? \
                   OR department LIKE ? \
                   OR position LIKE ? \
                '''
        search_pattern = f"%{search_term}%"
        results = self.db.execute_query("employees", query,
                                        (search_pattern, search_pattern, search_pattern, search_pattern, search_pattern,
                                         search_pattern))

        employees = []
        for row in results:
            employees.append({
                'id': row[0],
                'employee_id': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'email': row[4],
                'phone': row[5],
                'department': row[6],
                'position': row[7],
                'hire_date': row[8],
                'status': row[9],
                'created_at': row[10]
            })
        return employees

    def update_employee(self, employee_id, updates):
        set_clauses = []
        params = []

        for field, value in updates.items():
            set_clauses.append(f"{field} = ?")
            params.append(value)

        if not set_clauses:
            return False

        query = f"UPDATE employees SET {', '.join(set_clauses)} WHERE employee_id = ?"
        params.append(employee_id)

        try:
            self.db.execute_update("employees", query, params)
            return True
        except:
            return False

    def delete_employee(self, employee_id):
        query = "DELETE FROM employees WHERE employee_id = ?"
        try:
            self.db.execute_update("employees", query, (employee_id,))
            return True
        except:
            return False

    def get_employees_by_department(self, department):
        query = "SELECT * FROM employees WHERE department = ? ORDER BY last_name, first_name"
        results = self.db.execute_query("employees", query, (department,))

        employees = []
        for row in results:
            employees.append({
                'id': row[0],
                'employee_id': row[1],
                'first_name': row[2],
                'last_name': row[3],
                'email': row[4],
                'phone': row[5],
                'department': row[6],
                'position': row[7],
                'hire_date': row[8],
                'status': row[9],
                'created_at': row[10]
            })
        return employees

    def get_employee_count(self):
        query = "SELECT COUNT(*) FROM employees"
        result = self.db.execute_single("employees", query)
        return result[0] if result else 0