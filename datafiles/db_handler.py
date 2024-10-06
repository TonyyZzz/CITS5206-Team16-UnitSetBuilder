import csv
import sqlite3
import os

# Define the paths to the CSV files
course_csv_file = './datafiles/courses.csv'
unit_csv_file = './datafiles/units.csv'
specialisation_csv_file = './datafiles/specialisations.csv'

# Check if the database exists
if not os.path.exists('./instance/dev.db'):
    raise FileNotFoundError(
        "Database file not found.\nInitialise the database first.")

# Check the database structure
conn = sqlite3.connect('./instance/dev.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
if len(tables) == 0:
    raise ValueError("Broken database. No tables found.")


def truncate():
    conn.execute('DELETE FROM group_element')
    conn.execute('DELETE FROM "group"')
    conn.execute('DELETE FROM unit_set')
    conn.execute('DELETE FROM course_specialisation')
    conn.execute('DELETE FROM user')
    conn.execute('DELETE FROM unit')
    conn.execute('DELETE FROM specialisation')
    conn.execute('DELETE FROM course')
    conn.commit()
    conn.close()


def insert_data():
    # Read course data from CSV file excluding the header
    course_csv_data = []
    with open(course_csv_file, 'r', newline='', encoding='utf-8') as course_file:
        reader = csv.reader(course_file)
        next(reader)  # Skip the header
        for row in reader:
            course_csv_data.append(tuple(row))  # Append each row as a tuple

    # Read unit data from CSV file excluding the header
    unit_csv_data = []
    with open(unit_csv_file, 'r', newline='', encoding='utf-8') as unit_file:
        reader = csv.reader(unit_file)
        next(reader)  # Skip the header
        for row in reader:
            unit_csv_data.append(tuple(row))  # Append each row as a tuple

    # Read specialisation data from CSV file (no header line)
    specialisation_csv_data = []
    with open(specialisation_csv_file, 'r', newline='', encoding='utf-8') as specialisation_file:
        reader = csv.reader(specialisation_file)
        for row in reader:
            # Append each row as a tuple
            specialisation_csv_data.append(tuple(row))

    # Insert data into the database
    for Code, Title in course_csv_data:
        # cursor.execute('SELECT 1 FROM course WHERE code = ?', (Code,))
        # if cursor.fetchone() is None:
        #     cursor.execute('INSERT INTO course (code, title) VALUES (?, ?)', (Code, Title))
        # else:
        #     print(f"Code {Code} - {Title} already exists.")
        cursor.execute(
            'INSERT INTO course (code, title) VALUES (?, ?)', (Code, Title))

    for Code, Title, CreditPoints in unit_csv_data:
        cursor.execute('SELECT 1 FROM unit WHERE code = ?', (Code,))
        if cursor.fetchone() is None:
            cursor.execute(
                'INSERT INTO unit (code, name, credit_points) VALUES (?, ?, ?)', (Code, Title, CreditPoints))
        else:
            print(f"Code {Code} already exists, skipping insertion.")
        # cursor.execute('INSERT INTO unit (code, name, credit_points) VALUES (?, ?, ?)', (Code, Title, CreditPoints))

    for row in specialisation_csv_data:
        cursor.execute('INSERT INTO specialisation (name) VALUES (?)', row)

    # Add a test user account
    cursor.execute('INSERT INTO user (username, email, password_hash) VALUES (?, ?, ?)',
                   ('test', 'test@test.org', '$2b$12$MMPp3.O3TOZQW2nyzW5TfOsjwmAS21GKGF2p.EGGooCC4OuPmB0eS'))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Data has been written to the database.")


def is_empty():
    # count the number of rows in each table
    cursor.execute("SELECT COUNT(*) FROM course")
    course_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user")
    user_count = cursor.fetchone()[0]

    # return True if all tables are empty
    return course_count == 0 and user_count == 0


def check_run():
    if is_empty():
        insert_data()
    else:
        print("Data already exists in the database.")


if __name__ == '__main__':
    check_run()
