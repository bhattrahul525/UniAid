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
    "email": "zreh@example.com",
    "password": "123456789012",
    "mentor_id": null,
    "mentee_id": null
  }'

# Login
curl -X POST "http://127.0.0.1:8000/user/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "zreh@example.com",
    "password": "123456789012"
  }'

# Add/update profile: user_type is "mentor" or "mentee"; send mentor or mentee data accordingly.
# For both: creates profile if user has none, otherwise updates (upsert by user_id).

# Add or edit mentor profile (create if none, update if exists)
curl -X POST "http://127.0.0.1:8000/user/profile" `
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMDExIiwiZW1haWwiOiJ6cmVoQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTA4MDEzLCJleHAiOjE3NzM1MTE2MTN9.x5WanjV89Wh8OoEdsmkWs2uWuLQtjjhQZxbwFWAovS8" `
  -H "Content-Type: application/json" `
  -d '{
    "user_id": 1,
    "user_type": "mentor",
    "mentor": {
      "first_name": "Zreh",
      "last_name": "Sodaman",
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
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTAwNDk4LCJleHAiOjE3NzM1MDQwOTh9.MGoMsxWeFDe_-x-1Tyy9bnshWe1AocbOkfTl6qpyC7w" `
  -H "Content-Type: application/json" `
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
curl -X POST "http://127.0.0.1:8000/mentors" 
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTAwNDk4LCJleHAiOjE3NzM1MDQwOTh9.MGoMsxWeFDe_-x-1Tyy9bnshWe1AocbOkfTl6qpyC7w" `
  -H "Content-Type: application/json" `
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
curl -X PUT "http://127.0.0.1:8000/mentors/1" 
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTAwNDk4LCJleHAiOjE3NzM1MDQwOTh9.MGoMsxWeFDe_-x-1Tyy9bnshWe1AocbOkfTl6qpyC7w" `
  -H "Content-Type: application/json" `
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

#SESSION API CURLs

# Create session
curl -X POST "http://127.0.0.1:8000/sessions" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTAwNDk4LCJleHAiOjE3NzM1MDQwOTh9.MGoMsxWeFDe_-x-1Tyy9bnshWe1AocbOkfTl6qpyC7w" ^
  -d "{
    \"title\": \"TEST\",
    \"description\": \"Ask anything about our TEST\",
    \"mentor_id\": 1,
    \"session_type\": \"private\",
    \"scheduled_at\": \"2026-03-14T11:30:00Z\",
    \"user_ids\": [1, 2]
  }"

  # List sessions
  curl -X GET "http://127.0.0.1:8000/sessions"

  # Get session by ID
  curl -X GET "http://127.0.0.1:8000/sessions/1"

  # Update session
  curl -X PUT "http://127.0.0.1:8000/sessions/1" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZW1haWwiOiJqYW5lQGV4YW1wbGUuY29tIiwiaWF0IjoxNzczNTAwNDk4LCJleHAiOjE3NzM1MDQwOTh9.MGoMsxWeFDe_-x-1Tyy9bnshWe1AocbOkfTl6qpyC7w" ^
  -d "{
    \"title\": \"Updated title\",
    \"session_type\": \"private\",
    \"scheduled_at\": \"2026-03-15T18:30:00Z\",
    \"user_ids\": [2, 3]
  }"

  # Delete session
  curl -X DELETE "http://127.0.0.1:8000/sessions/1"
```

---

## Authenticated requests (optional)

If you add auth middleware later, use the token from login:

```bash
TOKEN="Bearer <paste_token_from_login_response>"

curl -X GET "http://127.0.0.1:8000/user/1" \
  -H "Authorization: $TOKEN"
```
