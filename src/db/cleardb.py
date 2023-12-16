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

# List of table names
table_names = [
    "survivor_locations",
    "bot",
    "bot_current_location",
    "obstacles",
    "tts_messages",
    "drive_commands"
]

# Clear the contents of each table
for table_name in table_names:
    delete_query = f"DELETE FROM {table_name};"
    cursor.execute(delete_query)
    print(f"Contents of '{table_name}' table cleared.")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Contents of all tables cleared successfully.")
