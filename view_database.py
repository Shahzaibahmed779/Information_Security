import sqlite3

def view_users():
    connection = sqlite3.connect('users.db')  # Connect to the database
    cursor = connection.cursor()

    # Fetch all data from the users table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Print column headers
    print("ID | Email                | Phone       | Password")
    print("-" * 50)

    # Print each row
    for row in rows:
        print(f"{row[0]:<2} | {row[1]:<20} | {row[2]:<12} | {row[3]}")

    connection.close()

if __name__ == "__main__":
    view_users()
