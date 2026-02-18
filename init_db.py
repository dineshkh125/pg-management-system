import sqlite3

conn = sqlite3.connect('database.db')

# Tenants Table
conn.execute('''
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT,
    rent INTEGER
)
''')

# Payments Table
conn.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id INTEGER,
    amount INTEGER,
    payment_date TEXT,
    expected_date TEXT,
    status TEXT,
    notes TEXT,
    receipt_number TEXT,
    FOREIGN KEY (tenant_id) REFERENCES tenants (id)
)
''')

conn.commit()
conn.close()

print("Database Updated Successfully!")
