# Database Guide - Payroll Management System

## 📍 Database Location

All databases are stored in the `databases/` folder in your project:

```
w:\Projects\payroll\databases\
```

### Database Files:

1. **admin.db** - Admin authentication data
2. **employees.db** - Employee information
3. **salary.db** - Salary records and history
4. **payroll.db** - Payroll processing records

---

## 🔍 How to View Database Data

### Method 1: Using the Custom Database Viewer (Recommended)

I've created a user-friendly database viewer for you!

**To run it:**
```bash
python db_viewer.py
```

**Features:**
- ✅ View all databases
- ✅ Browse tables and their structures
- ✅ View table data in formatted tables
- ✅ Run custom SQL queries
- ✅ See database file sizes

**Usage:**
1. Select a database (1-4)
2. Choose an option:
   - `v` - View table data
   - `s` - View table schema/structure
   - `r` - Run custom SQL query
   - `b` - Back to menu

---

### Method 2: Using PyCharm Database Tools

**Steps to connect in PyCharm:**

1. **Open Database Tool Window**
   - Go to `View` → `Tool Windows` → `Database`
   - Or press `Ctrl+Alt+Shift+S` (Windows)

2. **Add New Data Source**
   - Click the `+` icon
   - Select `Data Source` → `SQLite`

3. **Configure Connection**
   - **File:** Browse to `w:\Projects\payroll\databases\admin.db`
   - Click `Test Connection`
   - Click `OK`

4. **Repeat for other databases:**
   - `employees.db`
   - `salary.db`
   - `payroll.db`

5. **Browse Data**
   - Expand the database in the tree view
   - Double-click any table to view data
   - Right-click → `Export Data` to export

---

### Method 3: Using DB Browser for SQLite (External Tool)

**Download:** https://sqlitebrowser.org/

**Steps:**
1. Download and install DB Browser for SQLite
2. Open the application
3. Click `Open Database`
4. Navigate to `w:\Projects\payroll\databases\`
5. Select any `.db` file to view

**Features:**
- Visual table editor
- SQL query builder
- Data import/export
- Database structure visualization

---

### Method 4: Using SQLite Command Line

**Open SQLite database:**
```bash
cd w:\Projects\payroll\databases
sqlite3 employees.db
```

**Useful SQLite Commands:**
```sql
-- List all tables
.tables

-- Show table structure
.schema employees

-- View all data
SELECT * FROM employees;

-- Format output
.mode column
.headers on
SELECT * FROM employees;

-- Export to CSV
.mode csv
.output employees.csv
SELECT * FROM employees;
.output stdout

-- Exit SQLite
.quit
```

---

## 📊 Database Schema

### Admin Database (admin.db)

**Table: admins**
```
- id (INTEGER, PRIMARY KEY)
- username (TEXT, UNIQUE)
- password (TEXT)
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
```

**Default Admin:**
- Username: `admin`
- Password: `admin123`

---

### Employees Database (employees.db)

**Table: employees**
```
- id (INTEGER, PRIMARY KEY)
- employee_id (TEXT, UNIQUE)
- first_name (TEXT)
- last_name (TEXT)
- email (TEXT, UNIQUE)
- phone (TEXT)
- department (TEXT)
- position (TEXT)
- hire_date (TEXT)
- status (TEXT, default: 'active')
- created_at (TIMESTAMP)
```

---

### Salary Database (salary.db)

**Table: salaries**
```
- id (INTEGER, PRIMARY KEY)
- employee_id (TEXT, FOREIGN KEY)
- base_salary (REAL)
- allowances (REAL, default: 0)
- deductions (REAL, default: 0)
- effective_date (TEXT)
- created_at (TIMESTAMP)
```

---

### Payroll Database (payroll.db)

**Table: payroll_records**
```
- id (INTEGER, PRIMARY KEY)
- employee_id (TEXT)
- period (TEXT) - Format: YYYY-MM
- base_salary (REAL)
- allowances (REAL, default: 0)
- deductions (REAL, default: 0)
- net_salary (REAL)
- payment_date (TEXT)
- status (TEXT, default: 'processed')
- created_at (TIMESTAMP)
```

---

## 🔧 Useful SQL Queries

### View all employees with their departments
```sql
SELECT employee_id, first_name, last_name, department, position, status 
FROM employees 
ORDER BY department;
```

### Find employees in a specific department
```sql
SELECT * FROM employees 
WHERE department = 'IT';
```

### View salary history for an employee
```sql
SELECT * FROM salaries 
WHERE employee_id = 'EMP001' 
ORDER BY effective_date DESC;
```

### Calculate total payroll for a month
```sql
SELECT 
    period,
    COUNT(*) as employee_count,
    SUM(net_salary) as total_payroll,
    AVG(net_salary) as avg_salary
FROM payroll_records 
WHERE period = '2024-01'
GROUP BY period;
```

### Get employees with no salary set
```sql
SELECT e.employee_id, e.first_name, e.last_name, e.department
FROM employees e
LEFT JOIN salaries s ON e.employee_id = s.employee_id
WHERE s.id IS NULL;
```

---

## 🛠️ Backup and Restore

### Backup Database
```bash
# Copy the entire databases folder
xcopy /E /I w:\Projects\payroll\databases w:\Projects\payroll\databases_backup
```

### Restore Database
```bash
# Copy backup folder back
xcopy /E /I w:\Projects\payroll\databases_backup w:\Projects\payroll\databases
```

---

## 📝 Tips

1. **Always backup before making manual changes to databases**
2. **Use the app's built-in features for data manipulation when possible**
3. **The custom viewer (`db_viewer.py`) is safe - it won't modify data unless you run UPDATE/DELETE queries**
4. **Database files are small and fast - perfect for local development**
5. **You can open multiple databases simultaneously in PyCharm or DB Browser**

---

## 🚀 Quick Start

**To view your data right now:**

```bash
# Option 1: Use the custom viewer
python db_viewer.py

# Option 2: Use SQLite command line
cd databases
sqlite3 employees.db
.tables
SELECT * FROM employees;
```

---

**Need help?** The database viewer (`db_viewer.py`) is the easiest way to explore your data visually!
