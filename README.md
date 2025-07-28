
# KPA ERP - Backend API Implementation

This project is a backend API implementation for the **KPA ERP system**, built as part of a backend development assignment. It provides endpoints for managing form data, which can be consumed by the corresponding Flutter frontend application.

## Technologies & Tech Stack

The project is built using a modern and robust Python-based technology stack:

- **Backend Framework:** Django  
- **API Toolkit:** Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Configuration Management:** python-dotenv  
- **Python Version:** 3.10+  

## Implemented APIs

### 1. Create Wheel Specification

This endpoint allows for the submission of a new wheel specification form. It accepts a JSON payload and saves the data to the PostgreSQL database.

- **URL:** `/api/forms/wheel-specifications/`  
- **Method:** `POST`  

**Request Body:**

```json
{
  "formNumber": "WHEEL-2025-001",
  "submittedBy": "user_id_123",
  "submittedDate": "2025-07-03",
  "fields": {
    "treadDiameterNew": "915 (900-1000)",
    "lastShopIssueSize": "837 (800-900)",
    "condemningDia": "825 (800-900)",
    "wheelGauge": "1600 (+2,-1)",
    "variationSameAxle": "0.5",
    "variationSameBogie": "5",
    "variationSameCoach": "13",
    "wheelProfile": "29.4 Flange Thickness",
    "intermediateWWP": "20 TO 28",
    "bearingSeatDiameter": "130.043 TO 130.068",
    "rollerBearingOuterDia": "280 (+0.0/-0.035)",
    "rollerBearingBoreDia": "130 (+0.0/-0.025)",
    "rollerBearingWidth": "93 (+0/-0.250)",
    "axleBoxHousingBoreDia": "280 (+0.030/+0.052)",
    "wheelDiscWidth": "127 (+4/-0)"
  }
}
```

**Success Response (201 Created):**

```json
{
  "success": true,
  "message": "Wheel specification submitted successfully.",
  "data": {
    "formNumber": "WHEEL-2025-001",
    "submittedBy": "user_id_123",
    "submittedDate": "2025-07-03",
    "status": "Saved"
  }
}
```

---

### 2. Get Wheel Specifications

This endpoint retrieves a list of wheel specification forms. It supports filtering based on query parameters.

- **URL:** `/api/forms/wheel-specifications/`  
- **Method:** `GET`  

**Query Parameters (Optional):**

- `formNumber` (e.g., `WHEEL-2025-001`)  
- `submittedBy` (e.g., `user_id_123`)  
- `submittedDate` (e.g., `2025-07-03`)  

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Filtered wheel specification forms fetched successfully.",
  "data": [
    {
      "formNumber": "WHEEL-2025-001",
      "submittedBy": "user_id_123",
      "submittedDate": "2025-07-03",
      "fields": {
        "treadDiameterNew": "915 (900-1000)",
        "lastShopIssueSize": "837 (800-900)",
        "condemningDia": "825 (800-900)",
        "wheelGauge": "1600 (+2,-1)"
      }
    }
  ]
}
```

## Setup Instructions

### 1. Prerequisites

- Python 3.10 or higher installed  
- PostgreSQL server running  

### 2. Clone the Repository

```bash
git clone <your-repository-url>
cd <your-project-directory>
```

### 3. Create a Virtual Environment

```bash
# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Create a `requirements.txt` file with the following content:

```
Django
djangorestframework
psycopg2-binary
python-dotenv
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

### 5. Create Environment File

Create a `.env` file in the root directory:

```
SECRET_KEY='your-django-secret-key-here'
DEBUG=True

DB_NAME='kpa_erp_db'
DB_USER='your_postgres_user'
DB_PASSWORD='your_postgres_password'
DB_HOST='localhost'
DB_PORT='5432'
```

### 6. Configure `settings.py`

Import dotenv and load the environment variables:

```python
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('DB_NAME'),
    'USER': os.getenv('DB_USER'),
    'PASSWORD': os.getenv('DB_PASSWORD'),
    'HOST': os.getenv('DB_HOST'),
    'PORT': os.getenv('DB_PORT'),
  }
}
```

### 7. Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

The API will now be available at `http://127.0.0.1:8000`.

## ⚠️ Limitations & Assumptions

- **Development Environment:** Configured for local development; use `DEBUG=False` for production.
- **No Authentication:** All API endpoints are public and do not include authentication.
