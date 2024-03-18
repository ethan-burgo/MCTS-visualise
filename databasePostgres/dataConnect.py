import psycopg2

# Replace these variables with your PostgreSQL connection details
dbname = "MCTS_visualise"
user = "postgres"
password = "bindi2012"
host = "localhost"  # Usually "localhost" if the database is running locally
port = "5432"  # Usually 5432 by default

try:
    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    # Create a cursor object using the connection
    cursor = connection.cursor()

    # Execute a SQL query
    cursor.execute('SELECT * FROM "MCTS_visualise"."Execution"')

    # Fetch and print the query result
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    # Close the cursor and connection
    cursor.close()
    connection.close()

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL:", e)
