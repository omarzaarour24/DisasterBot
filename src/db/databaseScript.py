import psycopg2

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost",
    database="resQBot",
    user="postgres",
    #Nice
    port="69",
    password="0000"
)
print("connected to the database!")
# Define the table names
table_names = ["survivor_locations", "bot_current_location"]
# cursor = connection.cursor()
# cursor.execute(f"SELECT * FROM bot")
# rows = cursor.fetchall()
# for row in rows:
#          print(row)

# Iterate over the table names

for table_name in table_names:
    print(f"Table: {table_name}")
    print("-------------------")

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()

    # Execute a SELECT query to fetch all records from the table
    cursor.execute(f"SELECT * FROM "+table_name)

    # Fetch all the rows from the result set
    rows = cursor.fetchall()

    # Iterate over the rows and print the values
    for row in rows:
        print(row)

    print("\n")

# Close the cursor and the connection
cursor.close()
connection.close()
