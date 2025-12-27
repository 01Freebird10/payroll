# How to Fix the Corrupted payroll.db File

## The Problem

The `payroll.db` file is **corrupted** and is currently **locked by PyCharm** (or another application), preventing it from being deleted and recreated.

## Quick Fix Steps

### Step 1: Close PyCharm's Database Viewer

**In PyCharm:**
1. Look for the **Database** tool window (usually on the right side)
2. If `payroll.db` is connected, **right-click** on it
3. Select **"Close Connection"** or **"Remove Data Source"**
4. Or simply **close the payroll.db file tab** if it's open

**Alternative:** Just close PyCharm completely for a moment

### Step 2: Run the Fix Script

```bash
python fix_payroll_db.py
```

This script will:
- ✅ Delete the corrupted payroll.db file
- ✅ Create a fresh, empty payroll.db with the correct structure
- ✅ Verify the new database works

### Step 3: Run Your Application

```bash
python main.py
```

---

## What Happened?

The `payroll.db` file became corrupted (possibly due to an interrupted write or system crash). 

**Evidence:**
```
sqlite3.DatabaseError: file is not a database
```

This means the file exists but doesn't have valid SQLite database structure.

---

## If Fix Script Still Fails

If the file is still locked after closing PyCharm:

### Option A: Manual Delete
1. Close ALL applications that might have the file open
2. Navigate to: `w:\Projects\payroll\databases\`
3. Delete `payroll.db` manually
4. Run: `python fix_payroll_db.py`

### Option B: Restart Computer
Sometimes the file lock persists. A quick restart will clear it.

### Option C: Use Process Explorer (Advanced)
Download Process Explorer from Microsoft and find which process has the file open.

---

## After Fix

Once fixed, you can re-export the database:
```bash
python export_db_to_csv.py --all
```

This will export all databases including the newly created payroll.db to CSV format.
