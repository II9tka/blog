from rest_framework import serializers

from backend.chat.models import Chat


class ChatModelSerializer(serializers.ModelSerializer):
    creator = serializers.CharField(source='creator.username', read_only=True)

    class Meta:
        model = Chat
        fields = '__all__'
