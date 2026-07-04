# Campus Lost & Found

A web-based Lost & Found Management System designed for educational institutions. The platform enables students to report lost or found items, search existing reports, and helps administrators manage submissions through a centralized system.

The project follows a modular architecture with a Flask REST API backend and a React frontend. Future versions will include AI-assisted image matching and item recommendations.

---

## Project Architecture

```
campus-lost-found/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── utils/
│   ├── uploads/
│   └── database.db
│
└── frontend/   (planned)
```

### Backend Technologies

- Python
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask CORS
- SQLite

### Planned Frontend

- React
- Tailwind CSS

---

## Project Goal

The objective of this project is to provide a centralized platform for managing lost and found items within a campus environment.

The system is designed to:

- Allow users to report lost items.
- Allow users to report found items.
- Search and browse reports.
- Authenticate users securely using JWT.
- Provide administrative management of reports and users.
- Support future AI-powered image similarity matching.

---

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git

### Clone the Repository

```bash
git clone <repository-url>
cd campus-lost-found
```

### Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```cmd
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r backend/requirements.txt
```

---

## Configuration

Create a `.env` file inside the `backend/` directory.

```env
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DATABASE_URI=sqlite:///database.db
FLASK_DEBUG=false
```

---

## Running the Backend

Navigate to the backend directory:

```bash
cd backend
```

Start the Flask application:

```bash
python app.py
```

The API will be available at:

```
http://127.0.0.1:5000
```

---

## API Authentication

Protected endpoints require a JWT access token.

Include the following header in authenticated requests:

```http
Authorization: Bearer <JWT_TOKEN>
```

---

## License

This project is developed for educational purposes.
