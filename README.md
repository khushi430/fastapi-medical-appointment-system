# FastAPI Medical Appointment System
## 📌 Overview
This project is a backend API built using FastAPI to manage doctors, patients, and appointments.

## 🚀 Features
- Add and view doctors
- Add and view patients
- Book appointments
- Update and delete appointments
- Confirm and cancel appointments
- Filtering, sorting, and pagination

## 🛠 Tech Stack
- Python
- FastAPI
- Uvicorn
- Pydantic

## ▶️ How to Run
pip install fastapi uvicorn  
python -m uvicorn main:app --reload  

Open in browser:
http://127.0.0.1:8000/docs

## 📡 API Endpoints
- GET /doctors
- POST /doctors
- GET /patients
- POST /patients
- GET /appointments
- POST /appointments
- GET /appointments/browse
- PUT /appointments/{id}/confirm
- PUT /appointments/{id}/cancel
- DELETE /appointments/{id}

## 🎯 Learning Outcome
- Built REST APIs using FastAPI
- Implemented CRUD operations
- Applied filtering, sorting, and pagination
