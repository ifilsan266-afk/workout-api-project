# Workout Tracker API

## Description

A Flask REST API for managing workout sessions for personal trainers. Trainers can create and track workouts and their associated exercises. Each workout can include multiple exercises with sets, reps, or duration attached to each. Exercises are reusable across multiple workouts.

---

## Technologies Used

- Python 3.8+
- Flask 2.2.2
- Flask-SQLAlchemy 3.0.3
- Flask-Migrate 3.1.0
- Marshmallow 3.20.1
- Pipenv

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/workout-api.git
cd workout-api
```

### 2. Install dependencies

```bash
pipenv install
```

### 3. Activate the virtual environment

```bash
pipenv shell
```

### 4. Set up the database

```bash
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

### 5. Seed the database

```bash
python seed.py
```

### 6. Run the application

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000`

---

## API Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/workouts` | Get all workouts |
| POST | `/workouts` | Create a new workout |
| GET | `/workouts/<id>` | Get a single workout by ID |
| DELETE | `/workouts/<id>` | Delete a workout |

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/exercises` | Get all exercises |
| POST | `/exercises` | Create a new exercise |
| GET | `/exercises/<id>` | Get a single exercise by ID |
| DELETE | `/exercises/<id>` | Delete an exercise |

### Workout Exercises (Join Table)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/workout-exercises` | Add an exercise to a workout |

---

## Example Request Bodies

### POST /workouts
```json
{
  "name": "Morning Strength",
  "date": "2026-04-25"
}
```

### POST /exercises
```json
{
  "name": "Push Up",
  "muscle_group": "chest"
}
```

Valid `muscle_group` values: `chest`, `back`, `legs`, `shoulders`, `arms`, `core`, `full body`

### POST /workout-exercises
```json
{
  "workout_id": 1,
  "exercise_id": 2,
  "sets": 3,
  "reps": 12
}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 404 | Not Found |
