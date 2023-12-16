import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    port="69",
    database="resQBot",
    user="postgres",
    password="0000"
)
cursor = conn.cursor()

# Create the "survivor_locations" table
cursor.execute('''
    CREATE TABLE survivor_locations (
        id INTEGER,
        robotid INTEGER,
        cordx INTEGER,
        cordy INTEGER,
        timestamp TIMESTAMP,
        UNIQUE(cordx, cordy)
    )
''')

# Create the "bot" table
cursor.execute('''
    CREATE TABLE bot (
        id INTEGER,
        cordx INTEGER,
        cordy INTEGER,
        UNIQUE(cordx, cordy)
    )
''')

# Create the "bot_current_location" table
cursor.execute('''
    CREATE TABLE bot_current_location (
        id INTEGER,
        robotid INTEGER,
        cordx INTEGER,
        cordy INTEGER,
        UNIQUE(cordx, cordy)
    )
''')
# Create the "obstacles" table
cursor.execute('''
    CREATE TABLE obstacles (
        id INTEGER,
        robotid INTEGER,
        cordx INTEGER,
        cordy INTEGER,
        UNIQUE(cordx, cordy)
    )
''')
# Create the "tts_messages" table
cursor.execute('''
    CREATE TABLE tts_messages (
        id INTEGER PRIMARY KEY,
        robotid INTEGER,
        message TEXT,
        language TEXT
    )
''')


# Create the "drive_commands" table
cursor.execute('''
    CREATE TABLE drive_commands (
        id INTEGER,
        command_string TEXT,
        robotid INTEGER
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database tables created successfully.")
