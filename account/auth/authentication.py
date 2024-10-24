import re

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout

from ..models import CustomUser, UserProfile
from ..serializer import CustomUserSerializer, ProfileSerializer


# Login Authentication View
@api_view(["POST"])
def userLogin(request):
    """
    # User login function
    """
    credential = request.data.get("credential")
    password = request.data.get("password")

    if not credential or not password:
        return Response(
            {"message": "Invalid request. Both credential and password are required."},
            status=400,
        )

    is_email = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if re.match(is_email, credential):
        user = CustomUser.objects.get(email=credential)
        user.check_password(password)
    else:
        user = CustomUser.objects.get(username=credential)
        user.check_password(password)

    if user is not None:
        try:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response(
                {"message": "Login successful", "token": token.key},
                status=200,
            )
        except Exception as e:
            return Response({"message": f"An error occurred - {e}"}, status=400)
    else:
        return Response({"message": "authentication error"}, status=400)


@api_view(["POST"])
def userregistration(request):
    """
    Handling Registration of the Users

    """

    if request.method == "POST":
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            is_student = serializer.validated_data.get("is_student")
            field = serializer.validated_data.get("field")
            lastname = serializer.validated_data.get("last_name")
            firstname = serializer.validated_data.get("first_name")

            # filter for existing user
            if CustomUser.objects.filter(username=username).exists():
                return Response(
                    {"message": "Username already taken"},
                    status=400,
                )

            elif CustomUser.objects.filter(email=email).exists():
                return Response(
                    {"message": "Email associated with another account"},
                    status=400,
                )

            else:
                try:
                    new_user = CustomUser.objects.create_user(
                        last_name=lastname,
                        first_name=firstname,
                        username=username,
                        email=email,
                        password=password,
                        is_student=is_student,
                        is_active=True,
                        field=field,
                    )
                    serializer_user = CustomUserSerializer(new_user)
                    user = CustomUser.objects.get(username=username)
                    user.check_password(password)
                    token, created = Token.objects.get_or_create(user=user)
                    profile = UserProfile.objects.create(user=user)
                    login(request, user)
                    return Response(
                        {"message": "User sucessfully created", "token": token.key},
                        status=200,
                    )

                except Exception as e:
                    return Response(
                        {"message": f"Error occurred - {e}"},
                        status=400,
                    )

        else:
            return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    if request.method == "GET":
        user = request.user
        profile = UserProfile.objects.get(user=user)
        if profile is None:
            return Response({"message": "Profile not found for user"}, status=404)
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data, status=200)
