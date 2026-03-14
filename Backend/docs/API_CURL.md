# UniAid API – cURL examples

Base URL: `http://127.0.0.1:8000`

---

## Health & root

```bash
# Root
curl -X GET "http://127.0.0.1:8000/"

# Liveness
curl -X GET "http://127.0.0.1:8000/health"

# Database connectivity
curl -X GET "http://127.0.0.1:8000/db-health"
```

---

## User

```bash
# Register
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "securepass123",
    "mentor_id": null,
    "mentee_id": null
  }'

# Login
curl -X POST "http://127.0.0.1:8000/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane@example.com",
    "password": "securepass123"
  }'

# Add/update profile: user_type is "mentor" or "mentee"; send mentor or mentee data accordingly.
# For both: creates profile if user has none, otherwise updates (upsert by user_id).

# Add or edit mentor profile (create if none, update if exists)
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_type": "mentor",
    "mentor": {
      "first_name": "John",
      "last_name": "Smith",
      "mentor_type": "student",
      "university": "University of Toronto",
      "field_of_study": "Computer Science",
      "degree_level": "Masters",
      "years_in_country": 3,
      "visa_experience": 1,
      "housing_experience": 1,
      "cultural_adaptation_experience": 1,
      "career_guidance_experience": 0,
      "languages_spoken": "English,French",
      "availability_hours_per_week": 5,
      "sessions_completed": 0,
      "response_time_hours": 24,
      "graduation_year": 2024
    },
    "mentee": null
  }'

# Add or edit mentee profile (create if none, update if exists)
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "student",
      "home_country": "India",
      "preferred_destination_country": "Canada",
      "field_of_study": "Computer Science",
      "degree_level": "Masters",
      "budget_range": "medium",
      "preferred_language": "English"
    }
  }'

# Get user by ID
curl -X GET "http://127.0.0.1:8000/user/1"
```

---

## Mentors

```bash
# Create mentor (POST /mentors or POST /mentors/register)
curl -X POST "http://127.0.0.1:8000/mentors" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "mentor_type": "student",
    "university": "University of Toronto",
    "field_of_study": "Computer Science",
    "degree_level": "Masters",
    "years_in_country": 3,
    "visa_experience": 1,
    "housing_experience": 1,
    "cultural_adaptation_experience": 1,
    "career_guidance_experience": 0,
    "languages_spoken": "English,French",
    "availability_hours_per_week": 5,
    "sessions_completed": 10,
    "response_time_hours": 24,
    "graduation_year": 2024,
    "mentor_rating": 4.8
  }'

# List all mentors
curl -X GET "http://127.0.0.1:8000/mentors"

# Get mentor by ID
curl -X GET "http://127.0.0.1:8000/mentors/1"

# Update mentor (partial)
curl -X PUT "http://127.0.0.1:8000/mentors/1" \
  -H "Content-Type: application/json" \
  -d '{
    "availability_hours_per_week": 8,
    "mentor_rating": 4.9
  }'

# Delete mentor
curl -X DELETE "http://127.0.0.1:8000/mentors/1"
```

---

## Mentees

```bash
# Create mentee
curl -X POST "http://127.0.0.1:8000/mentees" \
  -H "Content-Type: application/json" \
  -d '{
    "user_type": "student",
    "home_country": "India",
    "preferred_destination_country": "Canada",
    "field_of_study": "Computer Science",
    "degree_level": "Masters",
    "budget_range": "medium",
    "preferred_language": "English"
  }'

# List all mentees
curl -X GET "http://127.0.0.1:8000/mentees"

# Get mentee by ID
curl -X GET "http://127.0.0.1:8000/mentees/1"

# Update mentee (partial)
curl -X PUT "http://127.0.0.1:8000/mentees/1" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_destination_country": "USA",
    "budget_range": "high"
  }'

# Delete mentee
curl -X DELETE "http://127.0.0.1:8000/mentees/1"
```

---

## Authenticated requests (optional)

If you add auth middleware later, use the token from login:

```bash
TOKEN="Bearer <paste_token_from_login_response>"

curl -X GET "http://127.0.0.1:8000/user/1" \
  -H "Authorization: $TOKEN"
```
