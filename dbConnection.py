import psycopg2

# Database connection details
DB_NAME = "my_local_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"  # Replace with your actual password
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to the database successfully!")
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None

# Test connection and fetch data
def fetch_students():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        conn.close()

# Run the function
fetch_students()
