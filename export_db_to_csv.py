import sqlite3
import csv
import os
from datetime import datetime


class DatabaseExporter:
    def __init__(self):
        self.db_dir = "databases"
        self.export_dir = "exported_data"
        self.databases = {
            'admin.db': 'Admin Database',
            'employees.db': 'Employees Database',
            'salary.db': 'Salary Database',
            'payroll.db': 'Payroll Database'
        }
        
        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            print(f"✓ Created export directory: {self.export_dir}")
    
    def get_tables(self, db_path):
        """Get all tables in the database"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            return [table[0] for table in tables]
        except sqlite3.DatabaseError as e:
            print(f"  ✗ Error reading database: {e}")
            return None
    
    def export_table_to_csv(self, db_path, table_name, output_file):
        """Export a table to CSV file"""
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all data
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Write to CSV
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(columns)
            # Write data
            writer.writerows(rows)
        
        conn.close()
        return len(rows)
    
    def export_database(self, db_file):
        """Export all tables from a database to CSV files"""
        db_path = os.path.join(self.db_dir, db_file)
        
        if not os.path.exists(db_path):
            print(f"✗ Database not found: {db_path}")
            return
        
        db_name = os.path.splitext(db_file)[0]
        db_export_dir = os.path.join(self.export_dir, db_name)
        
        # Create database-specific export directory
        if not os.path.exists(db_export_dir):
            os.makedirs(db_export_dir)
        
        print(f"\n{'='*70}")
        print(f"Exporting: {self.databases[db_file]}")
        print(f"{'='*70}")
        
        # Get all tables
        tables = self.get_tables(db_path)
        
        if tables is None:
            print(f"  ⚠️  SKIPPED: Database file is corrupted or not a valid SQLite database")
            return
        
        if not tables:
            print("  No tables found in this database.")
            return
        
        total_rows = 0
        for table in tables:
            output_file = os.path.join(db_export_dir, f"{table}.csv")
            row_count = self.export_table_to_csv(db_path, table, output_file)
            total_rows += row_count
            print(f"  ✓ {table:<30} → {row_count:>6} rows → {output_file}")
        
        print(f"\nTotal rows exported: {total_rows}")
    
    def export_all(self):
        """Export all databases"""
        print("\n" + "="*70)
        print("DATABASE EXPORTER - Payroll Management System".center(70))
        print("="*70)
        print(f"\nExport Location: {os.path.abspath(self.export_dir)}")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Export Time: {timestamp}\n")
        
        for db_file in self.databases.keys():
            self.export_database(db_file)
        
        print("\n" + "="*70)
        print("✓ Export Complete!".center(70))
        print("="*70)
        print(f"\nAll CSV files are saved in: {os.path.abspath(self.export_dir)}")
        print("\nYou can now:")
        print("  • Open CSV files in Excel, Google Sheets, or any spreadsheet app")
        print("  • Import them into PyCharm for viewing")
        print("  • Use them for data analysis")
        print("\n")
    
    def export_single_table(self, db_file, table_name):
        """Export a single table to CSV"""
        db_path = os.path.join(self.db_dir, db_file)
        
        if not os.path.exists(db_path):
            print(f"✗ Database not found: {db_path}")
            return
        
        # Check if table exists
        tables = self.get_tables(db_path)
        if table_name not in tables:
            print(f"✗ Table '{table_name}' not found in {db_file}")
            print(f"Available tables: {', '.join(tables)}")
            return
        
        db_name = os.path.splitext(db_file)[0]
        db_export_dir = os.path.join(self.export_dir, db_name)
        
        if not os.path.exists(db_export_dir):
            os.makedirs(db_export_dir)
        
        output_file = os.path.join(db_export_dir, f"{table_name}.csv")
        row_count = self.export_table_to_csv(db_path, table_name, output_file)
        
        print(f"\n✓ Exported {row_count} rows from '{table_name}' to:")
        print(f"  {os.path.abspath(output_file)}\n")
    
    def interactive_menu(self):
        """Interactive menu for selective export"""
        while True:
            print("\n" + "="*70)
            print("DATABASE EXPORTER - Interactive Mode".center(70))
            print("="*70)
            
            print("\nOptions:")
            print("  1. Export ALL databases (all tables)")
            print("  2. Export specific database")
            print("  3. Export specific table")
            print("  0. Exit")
            
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '0':
                print("\nExiting exporter. Goodbye!\n")
                break
            
            elif choice == '1':
                self.export_all()
                break
            
            elif choice == '2':
                print("\nAvailable Databases:")
                db_list = list(self.databases.keys())
                for i, (db_file, db_desc) in enumerate(self.databases.items(), 1):
                    print(f"  {i}. {db_desc} ({db_file})")
                
                db_choice = input("\nEnter database number: ").strip()
                try:
                    db_idx = int(db_choice) - 1
                    if 0 <= db_idx < len(db_list):
                        self.export_database(db_list[db_idx])
                    else:
                        print("Invalid choice!")
                except ValueError:
                    print("Please enter a valid number!")
            
            elif choice == '3':
                print("\nAvailable Databases:")
                db_list = list(self.databases.keys())
                for i, (db_file, db_desc) in enumerate(self.databases.items(), 1):
                    print(f"  {i}. {db_desc} ({db_file})")
                
                db_choice = input("\nEnter database number: ").strip()
                try:
                    db_idx = int(db_choice) - 1
                    if 0 <= db_idx < len(db_list):
                        db_file = db_list[db_idx]
                        db_path = os.path.join(self.db_dir, db_file)
                        tables = self.get_tables(db_path)
                        
                        print(f"\nAvailable Tables in {db_file}:")
                        for i, table in enumerate(tables, 1):
                            print(f"  {i}. {table}")
                        
                        table_choice = input("\nEnter table number: ").strip()
                        table_idx = int(table_choice) - 1
                        if 0 <= table_idx < len(tables):
                            self.export_single_table(db_file, tables[table_idx])
                        else:
                            print("Invalid table number!")
                    else:
                        print("Invalid database number!")
                except ValueError:
                    print("Please enter a valid number!")
            
            else:
                print("\nInvalid choice! Please try again.")


def main():
    """Main entry point"""
    exporter = DatabaseExporter()
    
    # Check if running with command line arguments
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            exporter.export_all()
        else:
            print("Usage:")
            print("  python export_db_to_csv.py         # Interactive mode")
            print("  python export_db_to_csv.py --all   # Export all databases")
    else:
        # Interactive mode
        exporter.interactive_menu()


if __name__ == "__main__":
    main()
