# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Sign up for activities as an authenticated teacher
- View participant lists without signing in
- Manage teacher accounts using hashed credentials in `teachers.json`

## Getting Started

1. Install the dependencies:

   ```
   pip install fastapi uvicorn
   ```

2. Add a teacher account. The password is requested securely and only its
   salted PBKDF2 hash is written to `src/teachers.json`:

   ```
   python src/create_teacher.py
   ```

3. Run the application from the repository root:

   ```
   uvicorn app:app --app-dir src --reload
   ```

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities and participant lists without signing in         |
| POST   | `/auth/login`                                                      | Log in with a teacher username and password                          |
| GET    | `/auth/me`                                                         | Get the current teacher session                                      |
| POST   | `/auth/logout`                                                     | End the current teacher session                                      |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up a student (teacher bearer token required)                    |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Unregister a student (teacher bearer token required)              |

Teacher passwords are never stored in plaintext. Keep `teachers.json` private
and only add accounts for assigned teachers. Sessions are held in memory and
expire after eight hours or when the server restarts.

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
