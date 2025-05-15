# Darshil-Yashvi-Devarsh ☁️ Cloud Service Access Management System

## 🔍 Overview


This is a **FastAPI-based backend system** designed to manage **access control for cloud APIs** using a **role-based subscription model**. Administrators can define subscription plans and API permissions, while users can subscribe to those plans to gain access to specific APIs.

## Team Members

- Darshil Gabani
- Yashvi Navadia
- Devarsh Jani

---

## Features

### 🔐 Role-Based Access Control

- Users are assigned roles (Admin or Customer).
- Access to APIs is determined based on role and subscription plan.
- Admins have elevated privileges to manage users, plans, and permissions.

---
  

Admins can create and manage access packages:

- **Create Plan** : `POST /plans` – Create a new subscription plan.
- **Update Plan** : `PUT /plans/{plan_id}` – Modify details of an existing plan.
- **Delete Plan** : `DELETE /plans/{plan_id}` – Remove a subscription plan.

---

### 🔑 Permission Management

Define and manage API-level access controls:

- **Add Permission** : `POST /permissions` – Add a new permission entry.
- **Update Permission** : `PUT /permissions/{permission_id}` – Update existing permission info.
- **Delete Permission** : `DELETE /permissions/{permission_id}` – Delete a permission.

---

### 👥 User Subscription Handling

- **Subscribe to a Plan** : `POST /subscriptions` – Customer subscribes to a plan.
- **Assign/Modify User Plan (Admin)** : `PUT /subscriptions/{user_id}` – Admin sets or updates a user's plan.
- **Check User Usage Limits** : `GET /usage/limit` – View current usage stats and limits for a user.

---

### Access Control and Usage Tracking (Cloud APIs)

- `GET /cloud/api1/{user_id}`
- `GET /cloud/api2/{user_id}`
- `GET /cloud/api3/{user_id}`
- `GET /cloud/api4/{user_id}`
- `GET /cloud/api5/{user_id}`
- `GET /cloud/api6/{user_id}`
  
---

## Tech Stack

- Python 3.13
- FastAPI
- SQLite with aiosqlite
- SQLAlchemy (Async ORM)
- Pydantic
- JWT for authentication

## Setup Instructions

1. Clone the Repository
   git clone https://github.com/darshilgabani/Darshil-Yashvi-Devarsh-Cloud-Access-System.git
   cd cloud-access-system
2. Create Virtual Environment
   python3 -m venv venv
   source venv/bin/activate
3. Install Requirements
   pip install -r requirements.txt
4. Run the Application
   uvicorn app.main:app --reload

5. Access API Docs

Visit: `http://127.0.0.1:8000/docs`
