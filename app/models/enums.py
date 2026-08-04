import enum


# Shared across models, schemas, and route-level role checks
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    ACCOUNTANT = "accountant"
