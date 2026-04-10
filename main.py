from fastapi import FastAPI
from pydantic import BaseModel
from database import SessionLocal
from models import StudentDB

app = FastAPI()

# Request body model
class Student(BaseModel):
    name: str
    age: int


# Home route
@app.get("/")
def home():
    return {"message": "welcome"}



# POST - Add student
@app.post("/students")
def add_student(student: Student):
    db = SessionLocal()

    new_student = StudentDB(
        name=student.name,
        age=student.age
    )

    db.add(new_student)
    db.commit()
    db.close()

    return {"message": "Saved successfully"}


# GET - Get all students
@app.get("/students")
def get_students():
    db = SessionLocal()

    data = db.query(StudentDB).all()

    db.close()
    return data


# PUT - Update student
@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    db = SessionLocal()

    existing = db.query(StudentDB).filter(StudentDB.id == student_id).first()

    if not existing:
        db.close()
        return {"error": "Student not found"}

    existing.name = student.name
    existing.age = student.age

    db.commit()
    db.close()

    return {"message": "Updated successfully"}
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()

    student = db.query(StudentDB).filter(StudentDB.id == student_id).first()

    if not student:
        db.close()
        return {"error": "Student not found"}

    db.delete(student)
    db.commit()
    db.close()

    return {"message": "Deleted successfully"}