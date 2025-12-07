import sqlite3

def repair():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # Check schema
    cursor.execute("PRAGMA table_info(items_requestitem)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"Columns: {columns}")
    
    if 'time_requested' not in columns:
        print("Column time_requested missing. Adding it...")
        try:
            # Add column (sqlite supports ADD COLUMN)
            cursor.execute("ALTER TABLE items_requestitem ADD COLUMN time_requested TEXT DEFAULT '12:00:00'")
            conn.commit()
            print("Column added.")
        except Exception as e:
            print(f"Failed to add column: {e}")
            
    # Update data just in case
    cursor.execute("UPDATE items_requestitem SET time_requested = '12:00:00' WHERE time_requested IS NULL OR time_requested = '1'")
    conn.commit()
    print("Data updated.")
    
    conn.close()

if __name__ == "__main__":
    repair()
