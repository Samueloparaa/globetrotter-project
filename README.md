# GlobeTrotter Travel Assistant — Phase 1: Monolith

A distributed travel recommendation application, built incrementally over the semester. This is **Phase 1**: a single monolithic REST API covering the core domain — users, destinations, itineraries, and basic recommendations. Later phases split this into microservices, add cloud deployment, and layer in caching/resilience.

## What it does

- Users can register and log in (JWT-based authentication).
- Users can browse available travel destinations.
- Authenticated users can create and view travel itineraries.
- Authenticated users can get basic personalized recommendations.

## Tech stack

- **Framework:** FastAPI
- **Auth:** JWT (JSON Web Tokens)
- **API docs:** Auto-generated Swagger UI at `/docs`

## How to run

1. Clone the repo and enter the project folder:
   ```
   git clone <your-repo-url>
   cd <project-folder>
   ```
2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   uvicorn main:app --reload
   ```
4. Open your browser to `http://127.0.0.1:8000/docs` to interact with the API via Swagger UI.

## Endpoints

| Method | Endpoint | Auth required | Description |
|--------|----------|----------------|-------------|
| POST | `/register` | No | Create a new user account |
| POST | `/login` | No | Log in and receive a JWT access token |
| GET | `/destinations` | No | List available travel destinations |
| GET | `/recommendations` | Yes | Get personalized destination recommendations |
| POST | `/itineraries` | Yes | Create a new travel itinerary |
| GET | `/itineraries` | Yes | List the logged-in user's itineraries |

### Authenticating in Swagger

1. Call `/register` to create an account, then `/login` to get an `access_token`.
2. Click the lock icon (**Authorize**) at the top of the `/docs` page.
3. Paste the token in and confirm.
4. All protected endpoints will now include your token automatically.

## Running tests

```
pytest
```

## Project status

This completes **Phase 1: Monolith** — a working, centralized REST API. It intentionally does not yet address scalability, fault tolerance, or containerized deployment; those are covered in Phases 2–4.
