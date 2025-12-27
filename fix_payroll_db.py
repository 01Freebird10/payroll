import sqlite3
import os
import time

def fix_payroll_db():
    """Fix corrupted payroll database"""
    db_path = os.path.join("databases", "payroll.db")
    
    print("="*70)
    print("PAYROLL DATABASE FIX UTILITY")
    print("="*70)
    
    # Check if file exists
    if os.path.exists(db_path):
        print(f"\n✓ Found database file: {db_path}")
        file_size = os.path.getsize(db_path)
        print(f"  File size: {file_size} bytes")
        
        # Try to test if it's a valid database
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            print("  ✓ Database is valid!")
            print("\n⚠️  Database appears to be working. No fix needed.")
            return
        except sqlite3.DatabaseError as e:
            print(f"  ✗ Database is corrupted: {e}")
            print("\n🔧 Attempting to fix...")
        
        # Close any existing connections
        try:
            conn.close()
        except:
            pass
        
        # Try to delete the file multiple times
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                os.remove(db_path)
                print(f"  ✓ Deleted corrupted database (attempt {attempt + 1})")
                break
            except PermissionError:
                if attempt < max_attempts - 1:
                    print(f"  ⚠️  File is locked, waiting... (attempt {attempt + 1})")
                    time.sleep(1)
                else:
                    print(f"\n✗ ERROR: Cannot delete file - it's locked by another process")
                    print("\n📌 SOLUTION:")
                    print("  1. Close PyCharm or any tool viewing payroll.db")
                    print("  2. Run this script again")
                    print("  3. Or manually delete: databases\\payroll.db")
                    return
    else:
        print(f"\n⚠️  Database file not found: {db_path}")
    
    # Create new database
    print("\n🔨 Creating fresh payroll database...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create payroll_records table (from database.py)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payroll_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            period TEXT NOT NULL,
            base_salary REAL NOT NULL,
            allowances REAL DEFAULT 0,
            deductions REAL DEFAULT 0,
            net_salary REAL NOT NULL,
            payment_date TEXT,
            status TEXT DEFAULT 'processed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("  ✓ Created payroll_records table")
    
    # Verify the new database
    print("\n✅ Verifying new database...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    
    print(f"  Tables found: {[t[0] for t in tables]}")
    print(f"  File size: {os.path.getsize(db_path)} bytes")
    
    print("\n" + "="*70)
    print("✅ SUCCESS! Payroll database has been recreated!")
    print("="*70)
    print("\nYou can now run: python main.py")

if __name__ == "__main__":
    try:
        fix_payroll_db()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
