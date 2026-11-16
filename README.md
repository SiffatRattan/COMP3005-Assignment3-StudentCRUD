# Assignment 3 - PostgreSQL Student CRUD Application

A command-line Python application that connects to a PostgreSQL database and implements all four required operations on the `students` table.

## Repository structure

```text
assignment3_starter/
├── app/
│   └── main.py              # CRUD functions and interactive menu
├── sql/
│   ├── 00_create_database.sql  # Create the PostgreSQL database
│   ├── 01_schema.sql           # Create the students table
│   └── 02_seed.sql             # Insert the three required students
├── .env.example             # Example database connection settings
├── .gitignore               # Excludes passwords and temporary files
├── requirements.txt         # Python dependencies
└── README.md                # Setup, operation, and demo instructions
```

## Prerequisites

- Python 3.10 or newer
- A working PostgreSQL server and pgAdmin
- Access credentials for the PostgreSQL server

## Step 1 - Create and populate the database in pgAdmin

1. Connect to the default `postgres` database in pgAdmin.
2. Open Query Tool and run `sql/00_create_database.sql` **once**. If `assignment_db` already exists, skip this step. Alternatively, create the database using pgAdmin's **Databases > Create > Database** menu.
3. Refresh Databases, connect to **assignment_db**, and open a new Query Tool on that database.
4. Run `sql/01_schema.sql`, then run `sql/02_seed.sql`.
5. Verify the starting table contents:

   ```sql
   SELECT * FROM students ORDER BY student_id;
   ```

   Expect three records: John Doe, Jane Smith, and Jim Beam, with the enrollment dates given in the assignment. IDs may differ if the table was used before.

The table has an auto-incrementing primary key, `NOT NULL` requirements for names and email, a `UNIQUE` email constraint, and a nullable `DATE` for enrollment.

## Step 2 - Install the application dependencies

Open a terminal in the repository root (the directory containing `requirements.txt`).

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` so it contains your actual database host, database name, username, and password. `.env` must **not** be committed to GitHub.

**Important if PostgreSQL is on a course VM:** `DB_HOST=127.0.0.1` only works when the Python application is running on the same machine as PostgreSQL, or when you've set up an SSH port-forward. Loading pgAdmin in a browser **does not** necessarily mean the PostgreSQL database is reachable from your laptop on port 5432. If the server accepts SSH, you can use a tunnel like this from your laptop:

```bash
ssh -N -L 5433:127.0.0.1:5432 YOUR_VM_USERNAME@YOUR_VM_IP
```

Leave that SSH session running, then set `DB_HOST=127.0.0.1` and `DB_PORT=5433` in `.env`. This example assumes PostgreSQL is listening on the VM's localhost port 5432. Alternatively, run the Python application directly on the database VM if Python and the dependencies are available there.

For the Carleton course VM setup, keep the university VPN connected and the SSH tunnel window open while using the app. Configure `.env` with `DB_NAME=assignment_db`, `DB_HOST=127.0.0.1`, and `DB_PORT=5433`. The PostgreSQL login is separate from SSH.

## Step 3 - Run the application

```bash
python app/main.py
```

The program shows a menu:

```text
1. Get all students
2. Add a student
3. Update a student's email
4. Delete a student
5. Exit
```

## Implemented functions

- `getAllStudents()`: Runs `SELECT` to retrieve and print all students, ordered by ID.
- `addStudent(first_name, last_name, email, enrollment_date)`: Uses a parameterized `INSERT` and prints the generated student ID.
- `updateStudentEmail(student_id, new_email)`: Uses a parameterized `UPDATE`, reporting whether the student exists.
- `deleteStudent(student_id)`: Uses a parameterized `DELETE`, reporting whether a record was removed.

The application handles invalid menu inputs and database errors. All SQL queries use placeholders rather than concatenating user input into SQL strings.

## Suggested demo (maximum 5 minutes)

1. Show pgAdmin connected to `assignment_db`. Display and execute `sql/01_schema.sql` and `sql/02_seed.sql` in Query Tool (both are safe to re-run for an existing setup), then run `SELECT * FROM students ORDER BY student_id;` to display the three initial students. Briefly show `sql/00_create_database.sql` to explain how the database was created.
2. In the application choose **1** to demonstrate `getAllStudents()`.
3. Choose **2** to add a test student: `Alex`, `Lee`, `alex.lee@example.com`, `2026-11-01`. **Write down the new student ID displayed by the program.**
4. Re-run the SELECT in pgAdmin to show the inserted student.
5. Choose **3** and update that student ID to `alex.lee.updated@example.com`. Re-run the SELECT in pgAdmin.
6. Choose **4** and delete that same student ID. Re-run the SELECT in pgAdmin to show removal.
7. Show the code structure or end the demo. Ensure the video is **5 minutes or less** and can be opened by a grader without requesting access.

## Demonstration video

**Video link:** REPLACE_WITH_YOUR_PUBLIC_OR_UNLISTED_SHAREABLE_VIDEO_URL

Replace the line above with your working video URL before submitting.

## GitHub / submission

1. Create a **public** GitHub repository for Assignment 3.
2. Commit the source code, database scripts, `requirements.txt`, `.gitignore`, `.env.example`, and this README. **Do not commit `.env` or any credentials.**
3. Add the demonstration video URL to this README and push that change.
4. Submit the **GitHub repository URL** through Brightspace. The video link should be in the README.
