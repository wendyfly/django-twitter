from accounts.api.serializers import UserSerializerForTweet
from rest_framework import serializers
from tweets.models import Tweet

#ModelSerializer: when you defined fields in Meta, all the fields don't need initialize
class TweetSerializer(serializers.ModelSerializer):
    #if we odn't declare user here, user will be an integer, userid
    user = UserSerializerForTweet()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'created_at', 'content')
