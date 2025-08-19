import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admin_auth import AdminAuth
from employee_manager import EmployeeManager
from salary_manager import SalaryManager
from database import Database
from utils import clear_screen, display_banner, get_valid_input, format_currency, format_date, create_separator


class PayrollSystem:
    def __init__(self):
        self.db = Database()
        self.admin_auth = AdminAuth(self.db)
        self.employee_manager = EmployeeManager(self.db)
        self.salary_manager = SalaryManager(self.db)
        self.current_admin = None

    def run(self):
        while True:
            clear_screen()
            display_banner()

            print("\n=== PAYROLL SYSTEM MAIN MENU ===")
            print("1. Admin Login")
            print("2. Exit System")

            choice = get_valid_input("Enter your choice (1-2): ", ["1", "2"])

            if choice == "1":
                if self.admin_login():
                    self.admin_menu()
            else:
                print("\nThank you for using the Payroll System!")
                break

    def admin_login(self):
        clear_screen()
        display_banner()
        print("\n=== ADMIN LOGIN ===")

        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        if self.admin_auth.authenticate(username, password):
            self.current_admin = username
            print(f"\nWelcome, {username}!")
            input("Press Enter to continue...")
            return True
        else:
            print("\nInvalid credentials! Access denied.")
            input("Press Enter to continue...")
            return False

    def admin_menu(self):
        while True:
            clear_screen()
            display_banner()
            print(f"\n=== ADMIN MENU - {self.current_admin} ===")
            print("1. Employee Management")
            print("2. Salary Management")
            print("3. Generate Reports")
            print("4. Logout")

            choice = get_valid_input("Enter your choice (1-4): ", ["1", "2", "3", "4"])

            if choice == "1":
                self.employee_menu()
            elif choice == "2":
                self.salary_menu()
            elif choice == "3":
                self.reports_menu()
            else:
                self.current_admin = None
                print("\nLogged out successfully!")
                input("Press Enter to continue...")
                break

    def employee_menu(self):
        while True:
            clear_screen()
            display_banner()
            print("\n=== EMPLOYEE MANAGEMENT ===")
            print("1. Add New Employee")
            print("2. View All Employees")
            print("3. Search Employee")
            print("4. Update Employee")
            print("5. Delete Employee")
            print("6. Back to Admin Menu")

            choice = get_valid_input("Enter your choice (1-6): ", ["1", "2", "3", "4", "5", "6"])

            if choice == "1":
                self.add_employee()
            elif choice == "2":
                self.view_all_employees()
            elif choice == "3":
                self.search_employee()
            elif choice == "4":
                self.update_employee()
            elif choice == "5":
                self.delete_employee()
            else:
                break

    def salary_menu(self):
        while True:
            clear_screen()
            display_banner()
            print("\n=== SALARY MANAGEMENT ===")
            print("1. Set Employee Salary")
            print("2. View Salary History")
            print("3. Process Payroll")
            print("4. Generate Payslip")
            print("5. Back to Admin Menu")

            choice = get_valid_input("Enter your choice (1-5): ", ["1", "2", "3", "4", "5"])

            if choice == "1":
                self.set_employee_salary()
            elif choice == "2":
                self.view_salary_history()
            elif choice == "3":
                self.process_payroll()
            elif choice == "4":
                self.generate_payslip()
            else:
                break

    def reports_menu(self):
        while True:
            clear_screen()
            display_banner()
            print("\n=== REPORTS ===")
            print("1. Monthly Payroll Report")
            print("2. Employee Summary Report")
            print("3. Salary Statistics")
            print("4. Back to Admin Menu")

            choice = get_valid_input("Enter your choice (1-4): ", ["1", "2", "3", "4"])

            if choice == "1":
                self.monthly_payroll_report()
            elif choice == "2":
                self.employee_summary_report()
            elif choice == "3":
                self.salary_statistics()
            else:
                break

    def add_employee(self):
        clear_screen()
        display_banner()
        print("\n=== ADD NEW EMPLOYEE ===")

        employee_data = {
            'first_name': input("Enter first name: ").strip(),
            'last_name': input("Enter last name: ").strip(),
            'email': input("Enter email: ").strip(),
            'phone': input("Enter phone number: ").strip(),
            'department': input("Enter department: ").strip(),
            'position': input("Enter position: ").strip(),
            'hire_date': input("Enter hire date (YYYY-MM-DD): ").strip(),
            'status': 'active'
        }

        if self.employee_manager.add_employee(employee_data):
            print("\nEmployee added successfully!")
        else:
            print("\nFailed to add employee.")

        input("Press Enter to continue...")

    def view_all_employees(self):
        clear_screen()
        display_banner()
        print("\n=== ALL EMPLOYEES ===")

        employees = self.employee_manager.get_all_employees()
        if employees:
            self.display_employees(employees)
        else:
            print("No employees found.")

        input("Press Enter to continue...")

    def search_employee(self):
        clear_screen()
        display_banner()
        print("\n=== SEARCH EMPLOYEE ===")

        search_term = input("Enter employee name, ID, or email: ").strip()
        employees = self.employee_manager.search_employee(search_term)

        if employees:
            self.display_employees(employees)
        else:
            print("No employees found matching your search.")

        input("Press Enter to continue...")

    def update_employee(self):
        clear_screen()
        display_banner()
        print("\n=== UPDATE EMPLOYEE ===")

        employee_id = input("Enter employee ID to update: ").strip()
        employee = self.employee_manager.get_employee_by_id(employee_id)

        if not employee:
            print("Employee not found.")
            input("Press Enter to continue...")
            return

        print(f"\nCurrent employee information:")
        self.display_employees([employee])

        print("\nEnter new information (leave blank to keep current value):")

        updates = {}
        fields = ['first_name', 'last_name', 'email', 'phone', 'department', 'position']

        for field in fields:
            current_value = employee.get(field, '')
            new_value = input(f"Enter {field.replace('_', ' ').title()} [{current_value}]: ").strip()
            if new_value:
                updates[field] = new_value

        if self.employee_manager.update_employee(employee_id, updates):
            print("\nEmployee updated successfully!")
        else:
            print("\nFailed to update employee.")

        input("Press Enter to continue...")

    def delete_employee(self):
        clear_screen()
        display_banner()
        print("\n=== DELETE EMPLOYEE ===")

        employee_id = input("Enter employee ID to delete: ").strip()
        employee = self.employee_manager.get_employee_by_id(employee_id)

        if not employee:
            print("Employee not found.")
            input("Press Enter to continue...")
            return

        print(f"\nEmployee to delete:")
        self.display_employees([employee])

        confirm = input("\nAre you sure you want to delete this employee? (yes/no): ").strip().lower()
        if confirm == 'yes':
            if self.employee_manager.delete_employee(employee_id):
                print("Employee deleted successfully!")
            else:
                print("Failed to delete employee.")
        else:
            print("Deletion cancelled.")

        input("Press Enter to continue...")

    def set_employee_salary(self):
        clear_screen()
        display_banner()
        print("\n=== SET EMPLOYEE SALARY ===")

        employee_id = input("Enter employee ID: ").strip()
        employee = self.employee_manager.get_employee_by_id(employee_id)

        if not employee:
            print("Employee not found.")
            input("Press Enter to continue...")
            return

        print(f"\nEmployee: {employee['first_name']} {employee['last_name']}")

        try:
            base_salary = float(input("Enter base salary: ").strip())
            allowances = float(input("Enter allowances: ").strip() or "0")
            deductions = float(input("Enter deductions: ").strip() or "0")
            effective_date = input("Enter effective date (YYYY-MM-DD): ").strip()

            if not effective_date:
                effective_date = datetime.now().strftime('%Y-%m-%d')

            salary_data = {
                'employee_id': employee_id,
                'base_salary': base_salary,
                'allowances': allowances,
                'deductions': deductions,
                'effective_date': effective_date
            }

            if self.salary_manager.set_salary(salary_data):
                print("\nSalary set successfully!")
            else:
                print("\nFailed to set salary.")

        except ValueError:
            print("\nInvalid salary amount. Please enter valid numbers.")

        input("Press Enter to continue...")

    def view_salary_history(self):
        clear_screen()
        display_banner()
        print("\n=== SALARY HISTORY ===")

        employee_id = input("Enter employee ID: ").strip()
        employee = self.employee_manager.get_employee_by_id(employee_id)

        if not employee:
            print("Employee not found.")
            input("Press Enter to continue...")
            return

        print(f"\nSalary history for {employee['first_name']} {employee['last_name']}:")

        salary_history = self.salary_manager.get_salary_history(employee_id)
        if salary_history:
            self.display_salary_history(salary_history)
        else:
            print("No salary history found.")

        input("Press Enter to continue...")

    def process_payroll(self):
        clear_screen()
        display_banner()
        print("\n=== PROCESS PAYROLL ===")

        period = input("Enter payroll period (e.g., 2024-01): ").strip()

        if not period:
            period = datetime.now().strftime('%Y-%m')

        confirm = input(f"Process payroll for period {period}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            result = self.salary_manager.process_payroll(period)
            if result:
                print(f"\nPayroll processed successfully for {result} employees.")
            else:
                print("\nFailed to process payroll.")
        else:
            print("Payroll processing cancelled.")

        input("Press Enter to continue...")

    def generate_payslip(self):
        clear_screen()
        display_banner()
        print("\n=== GENERATE PAYSLIP ===")

        employee_id = input("Enter employee ID: ").strip()
        period = input("Enter payroll period (YYYY-MM): ").strip()

        if not period:
            period = datetime.now().strftime('%Y-%m')

        payslip = self.salary_manager.generate_payslip(employee_id, period)

        if payslip:
            self.display_payslip(payslip)
        else:
            print("Failed to generate payslip.")

        input("Press Enter to continue...")

    def monthly_payroll_report(self):
        clear_screen()
        display_banner()
        print("\n=== MONTHLY PAYROLL REPORT ===")

        period = input("Enter period (YYYY-MM): ").strip()

        if not period:
            period = datetime.now().strftime('%Y-%m')

        report = self.salary_manager.get_monthly_payroll_report(period)

        if report:
            self.display_payroll_report(report, period)
        else:
            print("No data found for the specified period.")

        input("Press Enter to continue...")

    def employee_summary_report(self):
        clear_screen()
        display_banner()
        print("\n=== EMPLOYEE SUMMARY REPORT ===")

        employees = self.employee_manager.get_all_employees()

        if employees:
            self.display_employee_summary(employees)
        else:
            print("No employees found.")

        input("Press Enter to continue...")

    def salary_statistics(self):
        clear_screen()
        display_banner()
        print("\n=== SALARY STATISTICS ===")

        stats = self.salary_manager.get_salary_statistics()

        if stats:
            self.display_statistics(stats)
        else:
            print("No salary data available.")

        input("Press Enter to continue...")

    def display_employees(self, employees):
        print(create_separator('='))
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Position':<15} {'Status':<10}")
        print(create_separator('-'))

        for emp in employees:
            name = f"{emp['first_name']} {emp['last_name']}"
            print(
                f"{emp['employee_id']:<10} {name:<20} {emp['department']:<15} {emp['position']:<15} {emp['status']:<10}")

        print(create_separator('='))
        print(f"Total Employees: {len(employees)}")

    def display_salary_history(self, salary_history):
        print(create_separator('='))
        print(f"{'ID':<6} {'Base Salary':<12} {'Allowances':<11} {'Deductions':<11} {'Effective Date':<15}")
        print(create_separator('-'))

        for salary in salary_history:
            print(f"{salary['id']:<6} {format_currency(salary['base_salary']):<12} "
                  f"{format_currency(salary['allowances']):<11} {format_currency(salary['deductions']):<11} "
                  f"{format_date(salary['effective_date']):<15}")

        print(create_separator('='))

    def display_payslip(self, payslip):
        print(create_separator('='))
        print(f"PAYSLIP - {payslip['period']}")
        print(create_separator('-'))
        print(f"Employee: {payslip['first_name']} {payslip['last_name']}")
        print(f"ID: {payslip['employee_id']}")
        print(f"Department: {payslip['department']}")
        print(f"Position: {payslip['position']}")
        print(create_separator('-'))
        print(f"Base Salary: {format_currency(payslip['base_salary'])}")
        print(f"Allowances: {format_currency(payslip['allowances'])}")
        print(f"Deductions: {format_currency(payslip['deductions'])}")
        print(create_separator('-'))
        print(f"NET SALARY: {format_currency(payslip['net_salary'])}")
        print(f"Payment Date: {format_date(payslip['payment_date'])}")
        print(create_separator('='))

    def display_payroll_report(self, report, period):
        print(create_separator('='))
        print(f"MONTHLY PAYROLL REPORT - {period}")
        print(create_separator('-'))
        print(f"{'ID':<10} {'Name':<20} {'Department':<15} {'Base Salary':<12} {'Net Salary':<12}")
        print(create_separator('-'))

        total_payroll = 0
        for record in report:
            name = f"{record['first_name']} {record['last_name']}"
            print(f"{record['employee_id']:<10} {name:<20} {record['department']:<15} "
                  f"{format_currency(record['base_salary']):<12} {format_currency(record['net_salary']):<12}")
            total_payroll += record['net_salary']

        print(create_separator('-'))
        print(f"Total Employees: {len(report)}")
        print(f"Total Payroll: {format_currency(total_payroll)}")
        print(create_separator('='))

    def display_employee_summary(self, employees):
        print(create_separator('='))
        print("EMPLOYEE SUMMARY REPORT")
        print(create_separator('-'))

        department_count = {}
        total_employees = len(employees)

        for emp in employees:
            dept = emp['department']
            department_count[dept] = department_count.get(dept, 0) + 1

        print(f"Total Employees: {total_employees}")
        print(create_separator('-'))
        print("Department Breakdown:")
        for dept, count in department_count.items():
            print(f"  {dept}: {count} employees")

        print(create_separator('='))

    def display_statistics(self, stats):

        print("\nSalary Statistics")
        print("=" * 50)

        if not stats:
            print("No salary data available.")
            return


        def safe_currency(amount):
            if amount is None:
                return "$0.00"
            return f"${amount:,.2f}"

        print(f"Total Employees: {stats.get('total_employees', 0)}")
        print(f"Total Payroll: {safe_currency(stats.get('total_payroll'))}")
        print(f"Average Base Salary: {safe_currency(stats.get('avg_base_salary'))}")
        print(f"Minimum Base Salary: {safe_currency(stats.get('min_base_salary'))}")
        print(f"Maximum Base Salary: {safe_currency(stats.get('max_base_salary'))}")
        print(f"Average Net Salary: {safe_currency(stats.get('avg_net_salary'))}")

        print(f"\nDepartment Statistics:")
        dept_stats = self.salary_manager.get_department_salary_stats()
        if dept_stats:
            for dept in dept_stats:
                print(f"  {dept['department']}: {dept['employee_count']} employees, "
                      f"Avg: {safe_currency(dept.get('avg_base_salary'))}, "
                      f"Total: {safe_currency(dept.get('total_department_payroll'))}")
        else:
            print("  No department data available.")

        print("=" * 50)

if __name__ == "__main__":
    payroll_system = PayrollSystem()
    payroll_system.run()