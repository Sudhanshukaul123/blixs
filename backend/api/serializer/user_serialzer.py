from rest_framework import serializers
from api.models import User

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        feilds = "__all__"