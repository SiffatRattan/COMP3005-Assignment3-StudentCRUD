-- Connect to assignment_db before running this script.
-- Populate the table with the three students required by the assignment.
-- ON CONFLICT prevents duplicate emails if this file is accidentally rerun.
INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
    ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
    ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
    ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02')
ON CONFLICT (email) DO NOTHING;
