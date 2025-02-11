from django.core import serializers
from api.models import User

class UserSerializer(serializers.serialize):
    class Meta:
        model = User
        feilds = "__all__"