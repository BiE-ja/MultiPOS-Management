# 🛒 Multi-Point-of-Sale Management System – Fullstack App

> A modern and scalable fullstack application for managing one or multiple points of sale.  
> Built with FastAPI on the backend and React (Vite + Mantine UI + TypeScript) on the frontend.

---

## 📌 Project Status

This project is currently under **active development**.

### ✅ Already implemented

-   Some Data modeling (SQLAlchemy)
-   Pydantic schemas
-   Initial CRUD logic
-   JWT authentication
-   Some FastAPI routes
-   Frontend user management with React + Vite + Mantine

### 🔜 In Progress / Upcoming

-   User roles
-   Full API endpoints
-   Frontend implementation (React + Vite + Mantine UI)
-   Multi-store support
-   Real-time sales tracking
-   Analytics with Recharts

---

## 🧱 Tech Stack

### 🖥️ Backend

-   Python 3.11
-   FastAPI
-   SQLAlchemy
-   Pydantic
-   PostgreSQL
-   Alembic (planned)
-   Uvicorn
-   Docker

### 💻 Frontend _(planned)_

-   React + Vite
-   TypeScript
-   Mantine UI
-   TanStack Router
-   TanStack Query
-   Recharts
-   OpenAI SDK

---

## 🚀 Getting Started

### Backend (FastAPI)

```bash
# Clone the project
git clone https://github.com/BiE-ja/multipos-management.git
cd multipos-management

# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run dev server
uvicorn app.main:app --reload
API Docs available at: http://localhost:8000/docs

📂 Project Structure (WIP)
bash
Copier
Modifier
pos-management/
├── backend/           # (Python app - FastAPI)
│───app/
│   ├── core/          # Configuration, settings
│   ├── dto/           # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── crud/          # Business logic
│   ├── api/           # FastAPI routes
│   ├── deps/          # Dependencies
│   └── main.py        # App entry point
├── frontend/          # (React app - coming soon)
├── tests/
├── requirements.txt
├── .env
├── .gitignore
└── README.md
📊 Planned Features
🏪 Multi-store management

📦 Inventory & stock movement tracking

🧾 Sales, receipts, and invoice generation

📈 Real-time dashboards and analytics

🔐 Auth system with user roles and permissions

🧠 OpenAI-powered assistant for tasks & insights

☁️ Cloud sync & local offline support

🐳 Full Docker & CI/CD pipeline (GitHub Actions)

🤝 Contributing
Project is currently in a private active development phase.
Contributions will be open once MVP is ready 🚧

👤 Author
Built with passion by Brillant Eloge
GitHub: @BiE-ja

📝 License
To be defined.
```
