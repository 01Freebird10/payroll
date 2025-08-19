from datetime import datetime


class SalaryManager:
    def __init__(self, db):
        self.db = db

    def set_salary(self, salary_data):
        query = '''
                INSERT INTO salaries (employee_id, base_salary, allowances, deductions, effective_date)
                VALUES (?, ?, ?, ?, ?) \
                '''

        try:
            self.db.execute_update("salary", query, (
                salary_data['employee_id'],
                salary_data['base_salary'],
                salary_data['allowances'],
                salary_data['deductions'],
                salary_data['effective_date']
            ))
            return True
        except:
            return False

    def get_salary_history(self, employee_id):
        query = '''
                SELECT * \
                FROM salaries
                WHERE employee_id = ?
                ORDER BY effective_date DESC \
                '''
        results = self.db.execute_query("salary", query, (employee_id,))

        salaries = []
        for row in results:
            salaries.append({
                'id': row[0],
                'employee_id': row[1],
                'base_salary': row[2],
                'allowances': row[3],
                'deductions': row[4],
                'effective_date': row[5],
                'created_at': row[6]
            })
        return salaries

    def get_current_salary(self, employee_id):
        query = '''
                SELECT * \
                FROM salaries
                WHERE employee_id = ?
                ORDER BY effective_date DESC LIMIT 1 \
                '''
        result = self.db.execute_single("salary", query, (employee_id,))

        if result:
            return {
                'id': result[0],
                'employee_id': result[1],
                'base_salary': result[2],
                'allowances': result[3],
                'deductions': result[4],
                'effective_date': result[5],
                'created_at': result[6]
            }
        return None

    def update_salary(self, salary_id, updates):
        set_clauses = []
        params = []

        for field, value in updates.items():
            set_clauses.append(f"{field} = ?")
            params.append(value)

        if not set_clauses:
            return False

        query = f"UPDATE salaries SET {', '.join(set_clauses)} WHERE id = ?"
        params.append(salary_id)

        try:
            self.db.execute_update("salary", query, params)
            return True
        except:
            return False

    def delete_salary(self, salary_id):
        query = "DELETE FROM salaries WHERE id = ?"
        try:
            self.db.execute_update("salary", query, (salary_id,))
            return True
        except:
            return False

    def process_payroll(self, period):
        from employee_manager import EmployeeManager

        employee_manager = EmployeeManager(self.db)
        employees = employee_manager.get_all_employees()

        processed_count = 0

        for employee in employees:
            if employee['status'] != 'active':
                continue

            salary = self.get_current_salary(employee['employee_id'])
            if not salary:
                continue

            net_salary = salary['base_salary'] + salary['allowances'] - salary['deductions']

            query = '''
                    INSERT INTO payroll_records (employee_id, period, base_salary, allowances, deductions, net_salary)
                    VALUES (?, ?, ?, ?, ?, ?) \
                    '''

            try:
                self.db.execute_update("payroll", query, (
                    employee['employee_id'],
                    period,
                    salary['base_salary'],
                    salary['allowances'],
                    salary['deductions'],
                    net_salary
                ))
                processed_count += 1
            except:
                continue

        return processed_count

    def generate_payslip(self, employee_id, period):

        query = '''
                SELECT * \
                FROM payroll_records
                WHERE employee_id = ? \
                  AND period = ? \
                '''
        payroll_result = self.db.execute_single("payroll", query, (employee_id, period))

        if not payroll_result:
            return None


        from employee_manager import EmployeeManager
        employee_manager = EmployeeManager(self.db)
        employee = employee_manager.get_employee_by_id(employee_id)

        if not employee:
            return None


        return {
            'id': payroll_result[0],
            'employee_id': payroll_result[1],
            'period': payroll_result[2],
            'base_salary': payroll_result[3],
            'allowances': payroll_result[4],
            'deductions': payroll_result[5],
            'net_salary': payroll_result[6],
            'payment_date': payroll_result[7],
            'status': payroll_result[8],
            'first_name': employee['first_name'],
            'last_name': employee['last_name'],
            'department': employee.get('department', 'N/A'),
            'position': employee.get('position', 'N/A')
        }

    def get_monthly_payroll_report(self, period):
        query = '''
                SELECT * \
                FROM payroll_records
                WHERE period = ?
                ORDER BY employee_id \
                '''
        payroll_results = self.db.execute_query("payroll", query, (period,))

        from employee_manager import EmployeeManager
        employee_manager = EmployeeManager(self.db)

        records = []
        for payroll_row in payroll_results:
            employee_id = payroll_row[1]
            employee = employee_manager.get_employee_by_id(employee_id)

            if employee:
                records.append({
                    'id': payroll_row[0],
                    'employee_id': payroll_row[1],
                    'period': payroll_row[2],
                    'base_salary': payroll_row[3],
                    'allowances': payroll_row[4],
                    'deductions': payroll_row[5],
                    'net_salary': payroll_row[6],
                    'payment_date': payroll_row[7],
                    'status': payroll_row[8],
                    'first_name': employee['first_name'],
                    'last_name': employee['last_name'],
                    'department': employee.get('department', 'N/A'),
                    'position': employee.get('position', 'N/A')
                })

        return records

    def get_salary_statistics(self):
        query = '''
                SELECT COUNT(*)         as total_employees, \
                       AVG(base_salary) as avg_base_salary, \
                       MIN(base_salary) as min_base_salary, \
                       MAX(base_salary) as max_base_salary, \
                       AVG(net_salary)  as avg_net_salary, \
                       SUM(net_salary)  as total_payroll
                FROM payroll_records
                WHERE status = 'processed' \
                '''
        result = self.db.execute_single("payroll", query)

        if result:
            return {
                'total_employees': result[0],
                'avg_base_salary': result[1],
                'min_base_salary': result[2],
                'max_base_salary': result[3],
                'avg_net_salary': result[4],
                'total_payroll': result[5]
            }
        return None

    def get_department_salary_stats(self):

        query = '''
                SELECT * \
                FROM payroll_records
                WHERE status = 'processed' \
                '''
        payroll_results = self.db.execute_query("payroll", query)


        from employee_manager import EmployeeManager
        employee_manager = EmployeeManager(self.db)


        department_stats = {}

        for payroll_row in payroll_results:
            employee_id = payroll_row[1]
            employee = employee_manager.get_employee_by_id(employee_id)

            if employee:
                department = employee.get('department', 'Unassigned')
                base_salary = payroll_row[3]
                net_salary = payroll_row[6]

                if department not in department_stats:
                    department_stats[department] = {
                        'employee_count': 0,
                        'total_base_salary': 0,
                        'total_net_salary': 0
                    }

                department_stats[department]['employee_count'] += 1
                department_stats[department]['total_base_salary'] += base_salary
                department_stats[department]['total_net_salary'] += net_salary


        stats = []
        for department, data in department_stats.items():
            stats.append({
                'department': department,
                'employee_count': data['employee_count'],
                'avg_base_salary': data['total_base_salary'] / data['employee_count'],
                'total_department_payroll': data['total_net_salary']
            })


        stats.sort(key=lambda x: x['total_department_payroll'], reverse=True)

        return stats