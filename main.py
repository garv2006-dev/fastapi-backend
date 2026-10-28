import os

from fastapi import FastAPI, HTTPException, Path, Query
import json
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello")
def hello():
    return {"message": "Hello, FastAPI!"}

@app.get("/name")
def name():
    return {"name": "My Name Is Garv Variya"}


def load_data():
    with open("data.json", "r") as file:
        return json.load(file)

@app.get("/student")
def student():
    data = load_data()
    return data

@app.get("/student/{id}")
def get_student(id : int = Path(..., description="The ID of the student to retrieve")):
    data = load_data()
    for student in data:
        if student["student_id"] == id:
            return student
    raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")


@app.get("/filter")
def filter_students(course: str = Query(..., description="The course to filter students by")):
    data = load_data()
    filtered_students = [student for student in data if student["course"] == course]
    return filtered_students

sorted_students = ["age", "name","grade"]
order_options = ["asc", "desc"]

@app.get("/sort")
def sort_students(order: str = Query(None, description="The order to sort students by (asc or desc)"),
                  sort_by: str = Query(None, description="The field to sort students by age, name, or grade")):

    if sort_by not in sorted_students:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by value. Must be one of {sorted_students}")
    if order not in order_options:
        raise HTTPException(status_code=400, detail=f"Invalid order value. Must be one of {order_options}")
    data = load_data()
    return sorted(data, key=lambda student: student[sort_by], reverse=order == "desc")