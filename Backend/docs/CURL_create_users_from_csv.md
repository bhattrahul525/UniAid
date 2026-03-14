# CURL: Create users from users.csv (selected rows)

Base URL: `http://127.0.0.1:8000`

**Flow:** Run each "Register" first; use the `user_id` from the response in the matching "Add mentee profile" call.

---

## 1. Kavya Nguyen (CSV row 9)

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "kavya.nguyen@example.com", "password": "SecurePass123", "mentor_id": null, "mentee_id": null}'
```

**Add mentee profile** (set `user_id` to the value returned from register):
```bash
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "student",
      "home_country": "Indonesia",
      "preferred_destination_country": "Australia",
      "field_of_study": "Mechanical Engineering",
      "degree_level": "PhD",
      "budget_range": "55675",
      "preferred_language": "Japanese"
    }
  }'
```

---

## 2. Ivan Siddiqui (CSV row 16)

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "ivan.siddiqui@example.com", "password": "SecurePass123", "mentor_id": null, "mentee_id": null}'
```

**Add mentee profile:**
```bash
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 2,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "student",
      "home_country": "Vietnam",
      "preferred_destination_country": "Australia",
      "field_of_study": "Computer Science",
      "degree_level": "Bachelor",
      "budget_range": "30909",
      "preferred_language": "Hindi"
    }
  }'
```

---

## 3. Sana Rossi (CSV row 35)

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "sana.rossi@example.com", "password": "SecurePass123", "mentor_id": null, "mentee_id": null}'
```

**Add mentee profile:**
```bash
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 3,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "student",
      "home_country": "Nigeria",
      "preferred_destination_country": "Australia",
      "field_of_study": "Psychology",
      "degree_level": "Master",
      "budget_range": "37691",
      "preferred_language": "Mandarin"
    }
  }'
```

---

## 4. Abrar Müller (CSV row 67)

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "abrar.muller@example.com", "password": "SecurePass123", "mentor_id": null, "mentee_id": null}'
```

**Add mentee profile:**
```bash
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 4,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "parent",
      "home_country": "Japan",
      "preferred_destination_country": "Australia",
      "field_of_study": "Artificial Intelligence",
      "degree_level": "PhD",
      "budget_range": "42074",
      "preferred_language": "Mandarin"
    }
  }'
```

---

## 5. Ji-won Iqbal (CSV row 85)

**Register:**
```bash
curl -X POST "http://127.0.0.1:8000/user/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "jiwon.iqbal@example.com", "password": "SecurePass123", "mentor_id": null, "mentee_id": null}'
```

**Add mentee profile:**
```bash
curl -X POST "http://127.0.0.1:8000/user/profile" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 5,
    "user_type": "mentee",
    "mentor": null,
    "mentee": {
      "user_type": "student",
      "home_country": "China",
      "preferred_destination_country": "Australia",
      "field_of_study": "Psychology",
      "degree_level": "Master",
      "budget_range": "19726",
      "preferred_language": "Japanese"
    }
  }'
```

---

## Column mapping (CSV → API)

| CSV column              | API use                          |
|-------------------------|----------------------------------|
| first_name, last_name   | Used for email (first.last@…)    |
| user_type               | mentee.user_type (student/parent)|
| home_country            | mentee.home_country              |
| target_university       | → Australia (preferred_destination_country) |
| field_of_study          | mentee.field_of_study            |
| degree_level            | mentee.degree_level              |
| budget_range_aud        | mentee.budget_range              |
| preferred_language      | mentee.preferred_language        |

**Note:** Replace `user_id` (1, 2, 3, 4, 5) in each profile CURL with the actual `user_id` returned from the corresponding register response. If you run the registers in order, the first response will have `user_id: 1`, the second `user_id: 2`, and so on.
