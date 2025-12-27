import sqlite3
import os
from tabulate import tabulate


class DatabaseViewer:
    def __init__(self):
        self.db_dir = "databases"
        self.databases = {
            '1': ('admin.db', 'Admin Database'),
            '2': ('employees.db', 'Employees Database'),
            '3': ('salary.db', 'Salary Database'),
            '4': ('payroll.db', 'Payroll Database')
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_banner(self):
        print("\n" + "=" * 70)
        print("DATABASE VIEWER - Payroll Management System".center(70))
        print("=" * 70 + "\n")

    def get_tables(self, db_path):
        """Get all tables in the database"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        return [table[0] for table in tables]

    def get_table_data(self, db_path, table_name):
        """Get all data from a specific table"""
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        if rows:
            columns = rows[0].keys()
        else:
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
        
        conn.close()
        return columns, rows

    def get_table_schema(self, db_path, table_name):
        """Get table schema information"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        conn.close()
        return schema

    def display_table_schema(self, db_path, table_name):
        """Display table structure"""
        schema = self.get_table_schema(db_path, table_name)
        
        print(f"\n{'='*70}")
        print(f"Table Structure: {table_name}".center(70))
        print('='*70)
        
        headers = ["Column ID", "Name", "Type", "Not Null", "Default", "Primary Key"]
        schema_data = []
        
        for col in schema:
            schema_data.append([
                col[0],  # cid
                col[1],  # name
                col[2],  # type
                "Yes" if col[3] else "No",  # notnull
                col[4] if col[4] else "NULL",  # dflt_value
                "Yes" if col[5] else "No"  # pk
            ])
        
        print(tabulate(schema_data, headers=headers, tablefmt="grid"))

    def display_table_data(self, db_path, table_name):
        """Display table data"""
        columns, rows = self.get_table_data(db_path, table_name)
        
        print(f"\n{'='*70}")
        print(f"Table Data: {table_name}".center(70))
        print('='*70)
        
        if rows:
            # Convert rows to list of lists for tabulate
            data = [[row[col] for col in columns] for row in rows]
            print(tabulate(data, headers=columns, tablefmt="grid"))
            print(f"\nTotal Records: {len(rows)}")
        else:
            print("\nNo data found in this table.")

    def view_database(self, db_choice):
        """View a specific database"""
        db_file, db_name = self.databases[db_choice]
        db_path = os.path.join(self.db_dir, db_file)
        
        if not os.path.exists(db_path):
            print(f"\nDatabase file not found: {db_path}")
            input("\nPress Enter to continue...")
            return
        
        while True:
            self.clear_screen()
            self.display_banner()
            print(f"Viewing: {db_name} ({db_file})")
            print("\n" + "-" * 70)
            
            # Get all tables
            tables = self.get_tables(db_path)
            
            if not tables:
                print("\nNo tables found in this database.")
                input("\nPress Enter to continue...")
                return
            
            print("\nAvailable Tables:")
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")
            
            print("\nOptions:")
            print("  v - View table data")
            print("  s - View table schema/structure")
            print("  r - Run custom SQL query")
            print("  b - Back to database selection")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == 'b':
                break
            elif choice == 'v':
                table_num = input("Enter table number to view: ").strip()
                try:
                    table_idx = int(table_num) - 1
                    if 0 <= table_idx < len(tables):
                        self.clear_screen()
                        self.display_banner()
                        self.display_table_data(db_path, tables[table_idx])
                        input("\nPress Enter to continue...")
                    else:
                        print("Invalid table number!")
                        input("\nPress Enter to continue...")
                except ValueError:
                    print("Please enter a valid number!")
                    input("\nPress Enter to continue...")
            
            elif choice == 's':
                table_num = input("Enter table number to view schema: ").strip()
                try:
                    table_idx = int(table_num) - 1
                    if 0 <= table_idx < len(tables):
                        self.clear_screen()
                        self.display_banner()
                        self.display_table_schema(db_path, tables[table_idx])
                        input("\nPress Enter to continue...")
                    else:
                        print("Invalid table number!")
                        input("\nPress Enter to continue...")
                except ValueError:
                    print("Please enter a valid number!")
                    input("\nPress Enter to continue...")
            
            elif choice == 'r':
                self.run_custom_query(db_path)

    def run_custom_query(self, db_path):
        """Execute a custom SQL query"""
        self.clear_screen()
        self.display_banner()
        print("Custom SQL Query")
        print("-" * 70)
        print("Enter your SQL query (or 'cancel' to go back):")
        query = input("> ").strip()
        
        if query.lower() == 'cancel':
            return
        
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                if rows:
                    columns = rows[0].keys()
                    data = [[row[col] for col in columns] for row in rows]
                    print("\nQuery Results:")
                    print(tabulate(data, headers=columns, tablefmt="grid"))
                    print(f"\nTotal Records: {len(rows)}")
                else:
                    print("\nNo results found.")
            else:
                conn.commit()
                print(f"\nQuery executed successfully! Rows affected: {cursor.rowcount}")
            
            conn.close()
        except sqlite3.Error as e:
            print(f"\nSQL Error: {e}")
        
        input("\nPress Enter to continue...")

    def run(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            self.display_banner()
            
            print("Select Database to View:")
            print("-" * 70)
            for key, (db_file, db_name) in self.databases.items():
                db_path = os.path.join(self.db_dir, db_file)
                size = os.path.getsize(db_path) / 1024 if os.path.exists(db_path) else 0
                status = "✓" if os.path.exists(db_path) else "✗"
                print(f"  {key}. {db_name:<25} ({db_file}) [{status}] {size:.2f} KB")
            
            print("\n  0. Exit Viewer")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                print("\nExiting Database Viewer. Goodbye!")
                break
            elif choice in self.databases:
                self.view_database(choice)
            else:
                print("\nInvalid choice! Please try again.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    viewer = DatabaseViewer()
    viewer.run()
