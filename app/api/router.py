from fastapi import APIRouter

from app.api.routes import auth, faculty, fees, students, subjects, timetable, users

# One place that lists every route module, instead of main.py including each
# one separately. Each sub-router already carries its own prefix (e.g. /students).
api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(subjects.router)
api_router.include_router(students.router)
api_router.include_router(faculty.router)
api_router.include_router(timetable.router)
api_router.include_router(fees.router)
