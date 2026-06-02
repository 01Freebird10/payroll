#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import Database
from admin_auth import AdminAuth
from employee_manager import EmployeeManager
from salary_manager import SalaryManager


def test_system():
    print("Testing Payroll System...")

    # Test database initialization
    db = Database()
    print("[OK] Database initialized successfully")

    # Test admin authentication
    admin_auth = AdminAuth(db)
    assert admin_auth.authenticate('admin', 'admin123'), "Admin authentication failed"
    print("[OK] Admin authentication working")

    # Test employee management
    employee_manager = EmployeeManager(db)

    # Clean up existing test employee to ensure test is repeatable
    for emp in employee_manager.get_all_employees():
        if emp['email'] == 'john.doe@test.com':
            employee_manager.delete_employee(emp['employee_id'])

    # Add test employee
    test_employee = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@test.com',
        'phone': '123-456-7890',
        'department': 'IT',
        'position': 'Developer',
        'hire_date': '2024-01-01',
        'status': 'active'
    }

    result = employee_manager.add_employee(test_employee)
    assert result, "Failed to add employee"
    print("[OK] Employee addition working")

    # Get all employees
    employees = employee_manager.get_all_employees()
    assert len(employees) > 0, "No employees found"
    print(f"[OK] Employee retrieval working ({len(employees)} employees)")

    # Test salary management
    salary_manager = SalaryManager(db)

    # Set salary for the first employee
    if employees:
        salary_data = {
            'employee_id': employees[0]['employee_id'],
            'base_salary': 50000.0,
            'allowances': 5000.0,
            'deductions': 2000.0,
            'effective_date': '2024-01-01'
        }

        result = salary_manager.set_salary(salary_data)
        assert result, "Failed to set salary"
        print("[OK] Salary setting working")

        # Get salary history
        salary_history = salary_manager.get_salary_history(employees[0]['employee_id'])
        assert len(salary_history) > 0, "No salary history found"
        print("[OK] Salary history retrieval working")

        # Process payroll
        payroll_result = salary_manager.process_payroll('2024-01')
        assert payroll_result > 0, "Payroll processing failed"
        print(f"[OK] Payroll processing working ({payroll_result} employees)")

    print("\n[SUCCESS] All tests passed! The payroll system is working correctly.")


if __name__ == "__main__":
    test_system()