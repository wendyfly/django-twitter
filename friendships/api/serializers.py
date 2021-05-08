from accounts.api.serializers import UserSeriallizerForFriendship
from friendships.models import Friendship
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


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


class FriendshipSerializerForCreate(serializers.ModelSerializer):
    from_user_id = serializers.IntegerField()
    to_user_id = serializers.IntegerField()

    class Meta:
        model = Friendship
        fields = ('from_user_id', 'to_user_id')

    def validate(self, attrs):
        if not User.objects.filter(id= attrs['to_user_id']).exists():
            raise ValidationError({'message': 'to_user_id does not exist'})

        if not User.objects.filter(id=attrs['from_user_id']).exists():
            raise ValidationError({'message': 'from_user_id does not exist'})

        if attrs['from_user_id'] == attrs['to_user_id']:
            raise ValidationError({
                'message': 'from_user_id and to_user_id should be different'
            })

        if Friendship.objects.filter(
                from_user_id=attrs['from_user_id'],
                to_user_id=attrs['to_user_id'],
            ).exists():
            raise ValidationError({
                'message': 'already exists'
            })
        return attrs

    def create(self, validated_data):
        return Friendship.objects.create(
            from_user_id=validated_data['from_user_id'],
            to_user_id=validated_data['to_user_id'],
        )
