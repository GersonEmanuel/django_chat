from django.urls import path
from .views import ChatRoomView, MessageView

urlpatterns = [
	path('chats', ChatRoomView.as_view(), name='chats'),
	path('chats/<str:room_id>/messages', MessageView.as_view(), name='messages'),
	path('users/<int:user_id>/chats', ChatRoomView.as_view(), name='chatrooms'),
]