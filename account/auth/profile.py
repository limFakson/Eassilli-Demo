from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from ..models import UserProfile
from ..logic.storage import FirebaseStorage


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def profile_update(request):
    if request.method == "POST":
        try:
            data = request.data
            image = data["image"]
            user = request.user

            # Firebase initialise
            firebase = FirebaseStorage(file=image)
            image_url = firebase.store_file()

            profile = UserProfile.objects.update(image=image_url)
            return Response({"message": "Profile successfully updated"}, status=201)

        except Exception as e:
            return Response({"error": f"{e}"}, status=400)
