from accounts.api.serializers import UserSeriallizerForFriendship
from friendships.models import Friendship
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class FollowerSerializer(serializers.ModelSerializer):
    user = UserSeriallizerForFriendship(source='from_user')

    # if created_at is not in the above fields, it will try to find it in the model
    class Meta:
        model = Friendship
        fields = ('user', 'created_at')


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSeriallizerForFriendship(source='to_user')

    # if created_at is not in the above fields, it will try to find it in the model
    class Meta:
        model = Friendship
        fields = ('user', 'created_at')
