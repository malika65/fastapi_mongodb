from bson.objectid import ObjectId

from .database import student_collection, student_helper

# Retrieve all students present in the database
async def retrieve_students():
    students = await student_collection.find().to_list(1000)
    return students


# Add a new student into to the database
async def add_student(student_data: dict) -> dict:
    new_student = await student_collection.insert_one(student_data)
    created_student = await student_collection.find_one({"_id": new_student.inserted_id})     
    return created_student


# Retrieve a student with a matching ID
async def retrieve_one_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": id})
    return student

    
    
    
# Update a student with a matching ID
async def update_student_by_id(id: str, data: dict):
    if len(data) >= 1:
        update_result = await student_collection.update_one({"_id": id}, {"$set": data})
        if update_result.modified_count == 1:
            if (
                updated_student := await student_collection.find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await student_collection.find_one({"_id": id})) is not None:
        return existing_student

    


# Delete a student from the database
async def delete_student_by_id(id: str):
    student = await student_collection.find_one({"_id": id})
    if student:
        await student_collection.delete_one({"_id": id})
        return True