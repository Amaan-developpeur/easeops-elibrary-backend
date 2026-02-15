# EaseOps E-Library — User Backend

## 1. Project Overview

This project implements the user-facing backend for a simplified e-library system. It provides authentication, profile management, read-only access to books, and user interactions such as bookmarks and notes.

The scope of the assignment was limited to user-side functionality. Specifically:

* User registration and login (JWT-based)
* Profile preference management
* Listing and retrieving books
* Adding/removing bookmarks
* Creating and viewing personal notes
* Consistent API responses
* Basic logging and error handling

The following were intentionally excluded:

* Admin functionality (book creation, updates, deletion)
* Notifications (email/WhatsApp)
* Social sharing
* Chatbot or analytics features

The goal was to produce a clean, understandable backend with reasonable structure and safeguards, not a feature-complete production system.

---

## 2. Tech Stack

**Python + FastAPI**
Chosen for its minimal overhead, built-in request validation, dependency injection, and native OpenAPI support.

**SQLAlchemy (ORM)**
Used for database modeling and query abstraction. Provides explicit control over relationships and constraints without hiding SQL behavior.

**SQLite**
Used for simplicity and local execution. It keeps setup friction low for assessment purposes.

**Passlib (bcrypt)**
Used for password hashing. Passwords are never stored in plain text.

**python-jose (JWT)**
Used for token encoding and decoding.

**Pydantic**
Used for request validation and schema control.

**Logging (RotatingFileHandler)**
Basic file-based logging with rotation to avoid uncontrolled log growth.

No external caching, queuing, or background processing was introduced due to scope constraints.

---

## 3. Architecture Overview

### Folder Structure

```
app/
  core/        # Security, logging, response utilities
  db/          # Database setup and session management
  models/      # SQLAlchemy models
  routers/     # Route definitions grouped by domain
  schemas/     # Pydantic request/response schemas
  services/    # (Reserved for future business logic separation)
main.py        # Application entrypoint
```

### Separation of Concerns

* **Models** define database structure.
* **Schemas** define API input/output validation.
* **Routers** handle HTTP endpoints.
* **Core** contains cross-cutting concerns (security, logging, response formatting).
* **Database layer** handles session lifecycle and engine configuration.

No business logic is embedded directly inside models. Routers coordinate validation, persistence, and ownership checks.

### Request Flow (High-Level)

1. Client sends request.
2. FastAPI validates request via Pydantic schemas.
3. Dependency injection provides DB session and authenticated user (if required).
4. Router executes DB queries.
5. Response is wrapped in standardized success/error format.
6. Exceptions are handled globally and logged.

---

## 4. Implemented Features

### Authentication

* User registration with hashed password storage.
* Login using OAuth2PasswordRequestForm.
* JWT token generation with expiration.
* `/auth/me` endpoint for authenticated user retrieval.

### Authorization

* Protected routes use dependency-based JWT validation.
* Ownership checks ensure users can only access or modify their own bookmarks and notes.

### Core Domain Features

* Read-only book listing with:

  * Pagination
  * Category filtering
  * Text search
* Book detail retrieval.
* One bookmark per user per book (enforced by DB constraint).
* Multiple notes per user per book.
* User preference update (e.g., dark mode).

### Error Handling

* Global exception handler for HTTP errors.
* Global validation error handler.
* Catch-all 500 handler to avoid exposing stack traces.

### Logging

* Failed login attempts logged as warnings.
* Duplicate registration attempts logged.
* Unhandled exceptions logged as errors.
* Log rotation enabled.

### Response Standardization

All responses follow a consistent format:

Success:

```
{
  "success": true,
  "data": {...},
  "message": null
}
```

Error:

```
{
  "success": false,
  "error": "message"
}
```

This avoids mixed response shapes across endpoints.

---

## 5. Security Considerations

### Password Handling

* Passwords are hashed using bcrypt via Passlib.
* No plain text storage.

### JWT Strategy

* Short-lived access tokens.
* User ID stored in `sub` claim.
* Token required for protected endpoints.

### Ownership Checks

* Bookmark and note queries are filtered by both `user_id` and `book_id`.
* Users cannot access or modify another user's records.

### Database Constraints

* Unique constraint on `(user_id, book_id)` for bookmarks.
* Foreign keys enforce relational integrity.

### Secrets Management

* Sensitive values (e.g., `SECRET_KEY`) are loaded from environment variables.
* `.env` file is excluded from version control.

---

## 6. Assumptions & Tradeoffs

### Simplifications

* Tags stored as comma-separated strings instead of a normalized many-to-many table.
* SQLite used instead of PostgreSQL.
* No migrations tool (e.g., Alembic) introduced.
* No refresh tokens or token revocation logic.

### Why

The assignment scope emphasized user functionality and correctness over infrastructure depth.

Introducing additional layers (migrations, containerization, background jobs) would increase complexity without adding meaningful evaluation signal.

### What Would Change in Production

* Switch to PostgreSQL.
* Introduce Alembic migrations.
* Add structured logging (JSON logs).
* Implement refresh tokens and token revocation.
* Add rate limiting.
* Separate service layer for business logic.
* Normalize tags into separate tables.

---

## 7. How to Run

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create `.env` file:

```
DATABASE_URL=sqlite:///./easeops.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

The database file will be created automatically on startup.

---

## 8. API Usage Notes

Swagger UI is available at:

```
/docs
```

### Authentication Flow

1. Register user.
2. Click **Authorize**.
3. Enter:

   * `username` = email
   * `password` = password
4. Use protected endpoints.

The token is handled automatically by Swagger once authorized.

Protected routes:

* `/auth/me`
* `/user/profile`
* `/books/{id}/bookmark`
* `/books/{id}/notes`

---

## 9. Possible Improvements

* Replace SQLite with PostgreSQL.
* Normalize tags into separate relational tables.
* Introduce service layer abstraction.
* Add rate limiting middleware.
* Implement refresh tokens.
* Add structured logging (JSON + correlation IDs).
* Add automated tests for auth and ownership boundaries.
* Add pagination metadata (total count, next page).

---