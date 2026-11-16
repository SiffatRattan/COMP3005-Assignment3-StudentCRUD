"""Assignment 3: PostgreSQL CRUD application for the students table.

The public function names follow the exact names in the assignment.
SQL parameters use placeholders to avoid SQL injection.
"""

import os
from datetime import date

import psycopg
from dotenv import load_dotenv


# Load connection settings from a local .env file (not committed to GitHub).
load_dotenv()


def get_connection():
    """Open a PostgreSQL connection using the environment configuration."""
    return psycopg.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "assignment_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        connect_timeout=5,
    )


def getAllStudents():
    """Read and display every student, ordered by student ID."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT student_id, first_name, last_name, email, enrollment_date
                   FROM students
                   ORDER BY student_id;"""
            )
            students = cursor.fetchall()

    if not students:
        print("No students found.")
    else:
        print("\nID | First name | Last name | Email | Enrollment date")
        print("-" * 75)
        for student_id, first_name, last_name, email, enrollment_date in students:
            print(f"{student_id} | {first_name} | {last_name} | {email} | {enrollment_date}")
    return students


def addStudent(first_name, last_name, email, enrollment_date):
    """Insert one new student and return the automatically generated ID."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO students (first_name, last_name, email, enrollment_date)
                   VALUES (%s, %s, %s, %s)
                   RETURNING student_id;""",
                (first_name, last_name, email, enrollment_date),
            )
            student_id = cursor.fetchone()[0]

    print(f"Student added successfully! New student ID: {student_id}")
    return student_id


def updateStudentEmail(student_id, new_email):
    """Update an existing student's email; report if the ID does not exist."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """UPDATE students
                   SET email = %s
                   WHERE student_id = %s
                   RETURNING student_id;""",
                (new_email, student_id),
            )
            updated = cursor.fetchone()

    if updated is None:
        print(f"No student found with ID {student_id}.")
        return False
    print(f"Email updated successfully for student ID {student_id}.")
    return True


def deleteStudent(student_id):
    """Delete a student by ID; report whether a row was actually deleted."""
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """DELETE FROM students
                   WHERE student_id = %s
                   RETURNING student_id;""",
                (student_id,),
            )
            deleted = cursor.fetchone()

    if deleted is None:
        print(f"No student found with ID {student_id}.")
        return False
    print(f"Student ID {student_id} deleted successfully.")
    return True


def main():
    """Show a menu to run all four CRUD operations interactively."""
    while True:
        print("\n===== STUDENT DATABASE MENU =====")
        print("1. Get all students")
        print("2. Add a student")
        print("3. Update a student's email")
        print("4. Delete a student")
        print("5. Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                getAllStudents()
            elif choice == "2":
                first_name = input("First name: ").strip()
                last_name = input("Last name: ").strip()
                email = input("Email: ").strip()
                raw_date = input("Enrollment date (YYYY-MM-DD, or blank): ").strip()
                if not all((first_name, last_name, email)):
                    raise ValueError("First name, last name, and email cannot be blank.")
                enrollment_date = date.fromisoformat(raw_date) if raw_date else None
                addStudent(first_name, last_name, email, enrollment_date)
            elif choice == "3":
                student_id = int(input("Student ID to update: ").strip())
                new_email = input("New email: ").strip()
                if not new_email:
                    raise ValueError("New email cannot be blank.")
                updateStudentEmail(student_id, new_email)
            elif choice == "4":
                student_id = int(input("Student ID to delete: ").strip())
                deleteStudent(student_id)
            else:
                print("Invalid choice. Enter a number from 1 to 5.")
        except ValueError as error:
            print(f"Input error: {error}")
        except psycopg.Error as error:
            # A failed transaction is automatically rolled back by its context manager.
            print(f"Database error: {error}")
            print("Check your connection, table setup, and unique email constraint.")


if __name__ == "__main__":
    main()
