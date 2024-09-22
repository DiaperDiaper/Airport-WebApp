import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('airports.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS BayStands (
    id INTEGER PRIMARY KEY,
    airport_icao TEXT,
    stand_number TEXT,
    aircraft_type TEXT
)
''')

# Insert stand data for each airport
stands_data = [
    ('FACT', 'A3', 'light'),
    ('FACT', 'A4', 'light'),
    ('FACT', 'A5', 'light'),
    ('FACT', 'A6', 'medium'),
    ('FAOR', 'B1', 'light'),
    ('FAOR', 'B2', 'light'),
    # Add all other stands here...
    ('FAPE', 'A1', 'light'),
    ('FAGG', 'A1', 'light'),
    ('FALA', 'A1', 'light'),
    ('FABL', '1', 'light')
]

cursor.executemany('INSERT INTO BayStands (airport_icao, stand_number, aircraft_type) VALUES (?, ?, ?)', stands_data)

# Commit and close
conn.commit()
conn.close()
