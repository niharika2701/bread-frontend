# Module 14 - BREAD Frontend with Playwright E2E Tests

**IS 601 | Python for Web API | NJIT**

Builds on Module 13 by adding a full calculations front-end page with BREAD
operations, JWT-protected API routes, and Playwright E2E tests.

---

## Docker Hub

Image: `niharika2701/module14-bread-frontend:latest`

```bash
docker pull niharika2701/module14-bread-frontend:latest
```

Link: https://hub.docker.com/r/niharika2701/module14-bread-frontend

---

## Pages

| Route | Description |
|-------|-------------|
| /register | Register a new account |
| /login | Login and get JWT token |
| /calculations | BREAD page for calculations |

## API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| POST | /auth/register | Register user |
| POST | /auth/login | Login, returns JWT |
| POST | /calculations/ | Add calculation |
| GET | /calculations/ | Browse all calculations |
| GET | /calculations/{id} | Read one calculation |
| PUT | /calculations/{id} | Edit calculation |
| DELETE | /calculations/{id} | Delete calculation |

---

## How to Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run the app

```bash
DATABASE_URL="sqlite:///./local.db" python -m uvicorn main:app --reload
```

Open http://127.0.0.1:8000/register to create an account, then go to
http://127.0.0.1:8000/calculations to use the BREAD interface.

### 3. Run E2E tests

```bash
python -m pytest tests/test_calculations_e2e.py -v
```

The server starts automatically during tests. No manual setup needed.

---

## CI/CD Pipeline

GitHub Actions runs on every push:

1. **Test job** - installs Playwright, runs all 10 E2E tests
2. **Deploy job** - builds and pushes Docker image to Docker Hub on success
