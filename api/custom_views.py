from rest_framework.views import APIView
from django.contrib.auth import get_user_model

User = get_user_model()

#APIView compatible con los grupos de usuarios
class CustomAPIView(APIView):
    queryset = User.objects.none()

