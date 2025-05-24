from django.urls import path
from .views import UserView, LoginApiVIew, SignupApiView

urlpatterns = [
    path('users', UserView.as_view(), name='users'),
    path('login', LoginApiVIew.as_view(), name='login'),
    path('signup', SignupApiView.as_view(), name='signup')
]