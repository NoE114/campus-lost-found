# Campus Lost & Found Backend

This is the Flask-based REST API for the Campus Lost & Found project.

## 🚀 Getting Started

### Prerequisites
- Python 3.x installed
- Git
- Postman or cURL (for testing)

### 1. Setup the Environment
Clone the repository and set up your virtual environment:

```bash
# Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

2. Configure EnvironmentCreate a .env file in the backend/ folder (optional for local development, required for production):PlaintextJWT_SECRET_KEY=your_super_secret_key
DATABASE_URI=sqlite:///database.db

3. Run the ServerNavigate to the backend folder and run the application:Bashcd backend
python app.py
The server will start at http://127.0.0.1:5000.🛠 API DocumentationAuthenticationMethodEndpointDescriptionPOST/auth/registerRegister a new userPOST/auth/loginLogin to receive a JWT TokenLost ItemsMethodEndpointDescriptionPOST/lost/Report a lost item (Auth required)GET/lost/List all lost itemsGET/lost/search?category=...Filter items by categoryHow to AuthenticateMost routes require a JWT token. After logging in, include the token in your request headers:Header: AuthorizationValue: Bearer <YOUR_TOKEN_HERE>🧪 Testing with cURLTo register a user from your terminal:Bashcurl -X POST [http://127.0.0.1:5000/auth/register](http://127.0.0.1:5000/auth/register) ^
     -H "Content-Type: application/json" ^
     -d "{\"name\": \"Team Member\", \"email\": \"member@campus.edu\", \"password\": \"password123\"}"
📁 Project Structuremodels/: Database table definitions.routes/: API logic and endpoints.uploads/: Storage for item images.app.py: Application factory and entry point.
---


Database Sync: db.create_all()` runs automatically on startup, so they don't need to install MySQL yet.
* **Postman Collection:** If you are using Postman, you can export your collection as a JSON file and include it in the `docs/` folder of your project. This is a massive time-saver for teammates.

