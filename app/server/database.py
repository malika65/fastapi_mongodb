import motor.motor_asyncio
from decouple import config


MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_second_collection")



# helper function for parsing the results 
# from a database query into a Python dict.


# helpers


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "email": student["email"],
        "course": student["course"],
        "GPA": student["gpa"],
    }