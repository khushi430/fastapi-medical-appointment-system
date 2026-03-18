from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Medical Appointment System"}
doctors = [
    {"id": 1, "name": "Dr. Sharma", "specialization": "Cardiologist", "available": True},
    {"id": 2, "name": "Dr. Mehta", "specialization": "Dermatologist", "available": True}
]
patients = [
    {"id": 1, "name": "Khushi", "age": 21, "gender": "Female"},
    {"id": 2, "name": "Riya", "age": 22, "gender": "Female"}
]
appointments = []


@app.get("/doctors")
def get_doctors():
    return doctors
@app.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: int):
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return doctor
    return {"error": "Doctor not found"}





@app.get("/patients")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient_by_id(patient_id: int):
    for patient in patients:
        if patient["id"] == patient_id:
            return patient
    return {"error": "Patient not found"}
from pydantic import BaseModel

class Patient(BaseModel):
    name: str
    age: int
    gender: str


class Doctor(BaseModel):
    name: str
    specialization: str
    available: bool = True


class Appointment(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    status: str = "booked"

@app.post("/doctors")
def add_doctor(doctor: Doctor):
    new_doctor = {
        "id": len(doctors) + 1,
        "name": doctor.name,
        "specialization": doctor.specialization,
        "available": doctor.available
    }
    doctors.append(new_doctor)
    return {"message": "Doctor added", "doctor": new_doctor}

@app.post("/patients")
def add_patient(patient: Patient):
    new_patient = {
        "id": len(patients) + 1,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender
    }
    patients.append(new_patient)
    return {"message": "Patient added", "patient": new_patient}


@app.post("/appointments")
def book_appointment(appointment: Appointment):
    patient_found = False
    doctor_found = False

    # Check if patient exists
    for patient in patients:
        if patient["id"] == appointment.patient_id:
            patient_found = True
            break

    # Check if doctor exists
    for doctor in doctors:
        if doctor["id"] == appointment.doctor_id:
            doctor_found = True
            break

    if not patient_found:
        return {"error": "Patient not found"}

    if not doctor_found:
        return {"error": "Doctor not found"}

    new_appointment = {
        "id": len(appointments) + 1,
        "patient_id": appointment.patient_id,
        "doctor_id": appointment.doctor_id,
        "date": appointment.date,
        "status": appointment.status
    }

    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment": new_appointment
    }
@app.get("/appointments")
def get_appointments():
    return appointments

@app.get("/appointments/browse")
def browse_appointments(
    status: str = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = 1,
    limit: int = 5
):
    data = appointments.copy()

    # 🔍 Filter (search)
    if status:
        data = [a for a in data if a["status"].lower() == status.lower()]

    # 🔽 Sorting
    reverse = True if order == "desc" else False
    data = sorted(data, key=lambda x: x.get(sort_by, ""), reverse=reverse)

    # 📄 Pagination
    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(data),
        "results": data[start:end]
    }



@app.get("/appointments/{appointment_id}")
def get_appointment_by_id(appointment_id: int):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            return appointment
    return {"error": "Appointment not found"}


@app.put("/appointments/{appointment_id}")
def update_appointment(appointment_id: int, updated_data: Appointment):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment["patient_id"] = updated_data.patient_id
            appointment["doctor_id"] = updated_data.doctor_id
            appointment["date"] = updated_data.date
            appointment["status"] = updated_data.status
            return {"message": "Appointment updated", "appointment": appointment}

    return {"error": "Appointment not found"}


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointments.remove(appointment)
            return {"message": "Appointment deleted"}

    return {"error": "Appointment not found"}


@app.put("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment["status"] = "confirmed"
            return {"message": "Appointment confirmed", "appointment": appointment}

    return {"error": "Appointment not found"}


@app.put("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment["status"] = "cancelled"
            return {"message": "Appointment cancelled", "appointment": appointment}

    return {"error": "Appointment not found"}


