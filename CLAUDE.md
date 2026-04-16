# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Spendly** — A Flask-based expense tracking web application for Indian users (₹ rupee currency).

## Commands

```bash
# Run the application
python app.py              # Starts Flask dev server on port 5001

# Run tests
pytest                     # Run all tests
pytest -v                  # Verbose output
pytest tests/test_file.py  # Run specific test file
```

## Architecture

```
expense-tracker/
├── app.py              # Flask application entry point, all routes defined here
├── database/
│   ├── __init__.py     # Package init
│   └── db.py           # Database layer (students implement get_db, init_db, seed_db)
├── templates/          # Jinja2 HTML templates
│   ├── base.html       # Base template with navbar/footer
│   ├── landing.html    # Landing page
│   ├── login.html      # Login form
│   ├── register.html   # Registration form
│   ├── terms.html      # Terms and conditions
│   └── privacy.html    # Privacy policy
└── static/
    ├── css/style.css   # All styles
    └── js/main.js      # JavaScript (video modal, future features)
```

## Tech Stack

- **Backend:** Flask 3.1, Werkzeug 3.1
- **Database:** SQLite (via `database/db.py`) — foreign keys enabled
- **Testing:** pytest 8.3, pytest-flask
- **Frontend:** Vanilla JS, Google Fonts (DM Serif Display, DM Sans)

## Development Status

This is an educational project being built incrementally. Current state:

- ✅ Landing page, login, register routes (GET only)
- ✅ HTML templates for auth pages
- ⏳ Database layer — `db.py` is a stub; students implement `get_db()`, `init_db()`, `seed_db()`
- ⏳ Authentication — login/register forms lack POST handlers
- ⏳ Expense CRUD — placeholder routes only


## 🚦 Implemented vs Stub Routes

| Route                   | Method | Status        | Description                |
| ----------------------- | ------ | ------------- | -------------------------- |
| `/`                     | GET    | ✅ Implemented | Renders `landing.html`     |
| `/register`             | GET    | ✅ Implemented | Renders `register.html`    |
| `/login`                | GET    | ✅ Implemented | Renders `login.html`       |
| `/logout`               | GET    | ⏳ Stub        | Logout logic (Step 3)      |
| `/profile`              | GET    | ⏳ Stub        | User profile page (Step 4) |
| `/expenses/add`         | GET    | ⏳ Stub        | Add expense page (Step 7)  |
| `/expenses/<id>/edit`   | GET    | ⏳ Stub        | Edit expense (Step 8)      |
| `/expenses/<id>/delete` | GET    | ⏳ Stub        | Delete expense (Step 9)    |

⚠️ **Rule:** Do NOT implement stub routes unless the current task explicitly requires that step.

## Key Patterns

- **Database functions:** Students implement `get_db()` (returns SQLite connection with row_factory + foreign keys), `init_db()` (CREATE TABLE IF NOT EXISTS), `seed_db()` (sample data)
- **Templates:** Extend `base.html`; use `{% block title %}` and `{% block content %}`
- **Auth routes:** `/login`, `/register`, `/logout`
- **Expense routes:** `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` 

