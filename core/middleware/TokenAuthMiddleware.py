from fastapi import Request, HTTPException, Response
from starlette.middleware.base import BaseHTTPMiddleware
from rest_framework.authtoken.models import Token
from account.serializer import CustomUserSerializer
from asgiref.sync import sync_to_async
import os
import django

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()


class TokenAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, excluded_path):
        super().__init__(app)
        self.excluded_path = excluded_path or []

    async def dispatch(self, request: Request, call_next):
        # Exclude certain paths from the middleware
        if request.url.path in self.excluded_path:
            return await call_next(request)

        # Get token from Authorization header
        auth_token = request.headers.get("Authorization")
        if auth_token is None or not auth_token.startswith("Token "):
            return Response(
                status_code=403,
                content="Authentication credentials were not provided",
            )
        try:
            # Get token key from header
            key = auth_token.split("Token ")[1]

            # Fetch token object and user
            token_object = await sync_to_async(Token.objects.get)(key=key)
            user = await sync_to_async(lambda: token_object.user)()

            if not user.is_active:
                raise HTTPException(status_code=403, detail="User is inactive")
            # Serialize the user object
            serializer = await sync_to_async(CustomUserSerializer)(user)

            request.state.auth_user = serializer.data

            # Proceed with the request
            response = await call_next(request)
            return response

        except Token.DoesNotExist:
            raise HTTPException(status_code=403, detail="Invalid token")

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Server error: {e}")
