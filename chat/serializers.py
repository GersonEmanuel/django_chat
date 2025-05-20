from rest_framework import serializers
from chat.models import ChatRoom, ChatMessage
from user.serializers import UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    member = UserSerializer(many=True, read_only=True)
    members = serializers.ListField(write_only=True)

    def create(self, validated_data):
        member = validated_data.pop('members')
        chat_room = ChatRoom.objects.create(**validated_data)
        chat_room.member.set(member)
        return chat_room
    

    class Meta:
        model = ChatRoom
        exclude = ['id']

    
class ChatmessageSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        exclude = ['id', 'room']

        