from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from accounts.api.serializers import UserSerializer
from likes.models import Like
from comments.models import Comment
from tweets.models import Tweet
from django.contrib.contenttypes.models import ContentType


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('user', 'created_at')


class LikeSerializerForCreate(serializers.ModelSerializer):
    # only comment and tweet are valid content type
    content_type = serializers.ChoiceField(choices=['comment', 'tweet'])
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ('content_type', 'object_id')

    # same usage as ChoiceField
    def _get_model_class(self, data):
        if data['content_type'] == 'comment':
            return Comment
        if data['content_type'] == 'tweet':
            return Tweet
        return None

    # it will be triggered when the isValid method in the view is called
    def validate(self, data):
        model_class = self._get_model_class(data)
        if model_class is None:
            raise ValidationError({'content_type': 'Content type does not exist'})
        # get the first one which meet the filter; if there is no record, it will return null
        liked_object = model_class.objects.filter(id=data['object_id']).first()
        if liked_object is None:
            raise ValidationError({'object_id': 'Object does not exist'})
        return data

    def create(self, validated_data):
        model_class = self._get_model_class(validated_data)
        instance, _ = Like.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(model_class),
            object_id=validated_data['object_id'],
            user=self.context['request'].user,
        )
        return instance