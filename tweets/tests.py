from django.contrib.auth.models import User
from django.test import TestCase
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now


class TweetTests(TestCase):
    def test_hours_to_now(self):
        wendy = User.objects.create_user(username='wendy')
        tweet = Tweet.objects.create(user=wendy, content='hello world')
        tweet.created_at = utc_now() - timedelta(hours=10)
        tweet.save()
        self.assert_(tweet.hours_to_now, 10)
