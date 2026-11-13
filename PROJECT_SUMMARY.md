# Production-Ready Full-Stack Monorepo Architecture

**Tech Stack:** FastAPI (Backend) + React + Vite (Frontend) + PostgreSQL + Docker

This document outlines the industry-standard project structure for a professional, production-ready CRUD application. Keeping both the backend and frontend in a single monorepo with root-level Docker orchestration ensures seamless local development, easy CI/CD integration, and straightforward server deployment.

---

## 📁 Directory Layout

```text
my-crud-project/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # API route routers (v1 endpoints)
│   │   │   ├── v1/
│   │   │   │   ├── endpoints/
│   │   │   │   │   ├── auth.py
│   │   │   │   │   └── items.py
│   │   │   │   └── router.py
│   │   ├── core/             # App configurations, security, DB connections
│   │   │   ├── config.py     # Pydantic BaseSettings for env vars
│   │   │   ├── database.py   # SQLAlchemy session setup
│   │   │   └── security.py   # JWT / Password hashing
│   │   ├── models/           # SQLAlchemy ORM Database Models
│   │   │   └── user.py
│   │   ├── schemas/          # Pydantic Data Validation & Serialization Schemas
│   │   │   └── user.py
│   │   ├── crud/             # Database query helpers / Business logic
│   │   │   └── crud_user.py
│   │   └── main.py           # FastAPI app initialization & middleware
│   ├── tests/                # Pytest unit and integration tests
│   ├── Dockerfile            # Production container setup for FastAPI
│   ├── pyproject.toml        # Dependency management (or requirements.txt)
│   └── .env.example          # Template for environment variables
│
├── frontend/                 # React + Vite Application
│   ├── src/
│   │   ├── api/              # API client setup (Axios instances, endpoints)
│   │   │   ├── client.js
│   │   │   └── userService.js
│   │   ├── components/       # Reusable UI components (Buttons, Modals, Tables)
│   │   ├── layouts/          # Page layouts (Navbar, Sidebar, Footer)
│   │   ├── pages/            # Page-level views (Dashboard, Login, ItemList)
│   │   ├── context/          # React Context (Auth, Theme)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile            # Multi-stage build (Node build -> Nginx serve)
│   ├── nginx.conf            # Nginx production configuration for Vite SPA
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
├── docker-compose.yml        # Root orchestrator for local dev & production
└── README.md
```

---

## 🧩 Architectural Breakdown

### 1. Backend (`/backend/app`)

- **`core/`**: Houses global configurations. Use `pydantic-settings` to safely load environment variables (`DATABASE_URL`, `SECRET_KEY`) from `.env`.
- **`models/` vs `schemas/`**: Clearly separates responsibilities. `models/` defines how data looks in your SQL database (SQLAlchemy tables), while `schemas/` defines how data enters and leaves your API endpoints using Pydantic request/response validation.
- **`crud/`**: Keeps route handlers (`api/v1/endpoints/`) clean and focused by abstracting database queries into dedicated helper functions.

### 2. Frontend (`/frontend/src`)

- **`api/`**: Centralizes your HTTP client configuration (e.g., setting up an Axios instance with base URLs and automatic JWT header injection). Never hardcode `fetch` URLs directly inside UI components.
- **`pages/` vs `components/`**: `pages` represent full route views, whereas `components` are smaller, reusable UI pieces (such as data tables or form inputs).

---

## 🐳 Production Deployment Configuration

### Frontend Production Dockerfile (`frontend/Dockerfile`)

React Vite applications compile into static HTML/JS/CSS assets. Use a **multi-stage build** so Node compiles the code, and a lightweight Nginx server serves it:

```dockerfile
# Stage 1: Build the React application
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx Configuration (`frontend/nginx.conf`)

Crucial for Single Page Applications (SPAs) to ensure React Router handles client-side routing properly on refresh:

```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
}
```

### Root Orchestration (`docker-compose.yml`)

For production deployment on a VPS (such as an Ubuntu server via Docker), spin up your database, backend, and frontend together:

```yaml
version: "3.8"

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    restart: always
    environment:
      - DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
    depends_on:
      - db
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  postgres_data:
```
