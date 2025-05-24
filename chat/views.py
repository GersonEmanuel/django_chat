from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from .serializers import ChatRoomSerializer, ChatmessageSerializer
from .models import ChatRoom, ChatMessage
# Create your views here.

class ChatRoomView(APIView):
    def get(self, request, user_id):
        chat_rooms = ChatRoom.objects.filter(member=user_id)
        serializer = ChatRoomSerializer(
            chat_rooms,
            many=True,
            context={"request":request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serialzer = ChatRoomSerializer(
            data=request.data,
            context={"request":request}
        )
        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status=status.HTTP_200_OK)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MessageView(ListAPIView):
    serializer_class = ChatmessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return ChatMessage.objects.filter(chat_roomId=room_id).order_by('-timestamp')
