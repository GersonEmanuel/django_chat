from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import (
    UserSerializer, LoginSerializer, SignupSerializer
)

# Create your views here.

class UserView(CreateAPIView):
    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        exclude_users_id = []
        try:
            exclude_users = self.request.query_params.get('exclude')
            if exclude_users:
                users_id = exclude_users.split(',')
                for user in users_id:
                    exclude_users_id.append(int(user))
        except:
            return []
        return super().get_queryset().exlude(id__in=exclude_users_id)
    




class LoginApiVIew(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer



class SignupApiView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = SignupSerializer
