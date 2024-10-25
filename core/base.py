from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, Response
from . import session
from account.models import CustomUser
from .session import UserModel, RegisterUser
from django.http.response import JsonResponse
import re


router = APIRouter()


@router.get("/user")
def user():
    user = CustomUser.objects.all()
    return {"data": list(user.values())}


@router.post("/reg", status_code=201)
def demo(user: RegisterUser):
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    try:
        if CustomUser.objects.filter(username=user.userName).exists():
            return HTTPException(
                detail={"message": "user already exists"}, status_code=401
            )
        elif not re.fullmatch(email_regex, user.email):
            return HTTPException(detail={"message": "invalid email"}, status_code=401)
        elif CustomUser.objects.filter(email=user.email).exists():
            return HTTPException(
                detail={"message": "email already exists"}, status_code=401
            )
        else:
            user = CustomUser.objects.create(
                username=user.userName,
                email=user.email,
                last_name=user.lastName,
                first_name=user.firstName,
                is_student=user.isStudent,
                is_active=True,
                field=user.field,
            )

            # ser password
            user.set_password(user.password)
            user.save()

            return {"items": user}
    except Exception as e:
        return {"error": f"error occurred - {e}"}

