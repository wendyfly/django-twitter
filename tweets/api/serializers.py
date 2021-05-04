from accounts.api.serializers import UserSerializerForTweet
from rest_framework import serializers
from tweets.models import Tweet


# ModelSerializer: when you defined fields in Meta, all the fields don't need initialize
class TweetSerializer(serializers.ModelSerializer):
    # if we odn't declare user here, user will be an integer, userid
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')


class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
