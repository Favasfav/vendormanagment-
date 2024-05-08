Vendor Management System
This is a Django-based Vendor Management System API.

Description
The Vendor Management System API allows users to manage vendors, purchase orders, and track vendor performance. It provides endpoints for user authentication, vendor CRUD operations, purchase order management, and vendor performance tracking.

Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your/repository.git
Install dependencies:
bash
Copy code
pip install -r requirements.txt
Apply migrations:
bash
Copy code
python manage.py migrate
Start the development server:
Copy code
python manage.py runserver
Usage
API Endpoints
Authentication:
POST /api/token/: Obtain JWT token for authentication.
POST /api/token/refresh/: Refresh JWT token.
Vendors:
POST /api/vendor/: Create a new vendor.
GET /api/vendor/: Retrieve all vendors.
GET /api/vendor/<int:pk>/: Retrieve a specific vendor.
PUT /api/vendor/<int:pk>/: Update a specific vendor.
DELETE /api/vendor/<int:pk>/: Delete a specific vendor.
Purchase Orders:
POST /api/purchaseorder/: Create a new purchase order.
GET /api/purchaseorder/: Retrieve all purchase orders.
GET /api/purchaseorder/<int:pk>/: Retrieve a specific purchase order.
PUT /api/purchaseorder/<int:pk>/: Update a specific purchase order.
DELETE /api/purchaseorder/<int:pk>/: Delete a specific purchase order.
Vendor Performance:
GET /api/vendors/<int:pk>/performance/: Retrieve performance metrics for a specific vendor.
Contribut
