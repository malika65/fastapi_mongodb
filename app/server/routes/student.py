from typing import List
from fastapi import APIRouter, Body, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from server.crud import (
    add_student,
    delete_student_by_id,
    retrieve_one_student,
    retrieve_students,
    update_student_by_id
)

from server.schemas import (
    ErrorResponseModel,
    ResponseModel,
    StudentModel,
    UpdateStudentModel,
    
)

router = APIRouter()

from server.database import student_collection


@router.get("/", response_description="List all students", response_model=List[StudentModel])
async def list_students():
    students = await retrieve_students()
    return students

@router.post("/", response_description="Add new student", response_model=StudentModel)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    created_student = await add_student(student)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_student)

@router.get("/{id}", response_description="Get a single student", response_model=StudentModel)
async def show_student(id: str):

    if (student := await retrieve_one_student(id) ) is not None:
        return student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

@router.put("/{id}", response_description="Update a student", response_model=StudentModel)
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}
    updated_stud = await update_student_by_id(id, student)
    if updated_stud:
        return  updated_stud
    raise HTTPException(status_code=404, detail=f"Student {id} not found")




@router.delete("/{id}", response_description="Delete a student")
async def delete_student(id: str):

    delete_result = await delete_student_by_id(id)
    if delete_result:
        return {
            "msg":"Student with ID: {id} removed. Student deleted successfully",
            "status": status.HTTP_204_NO_CONTENT
            }

    raise HTTPException(status_code=404, detail=f"Student {id} not found")