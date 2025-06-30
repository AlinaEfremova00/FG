from rest_framework import serializers
from users.models import User, Follow
from .serializers import UserSerializer


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('user', 'author')
