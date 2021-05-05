from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now


class Tweet(models.Model):
    # who post this tweet
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        help_text='who posts this tweet',
    );  # if it's foreign key, we have to set_null on_delete
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # used to sort the tweet, auto add

    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')

    @property  # when we call this funciton , don't need to have parenthsis
    def hours_to_now(self):
        # datetime.now 不带时区信息，需要增加上 utc 的时区信息
        return (utc_now() - self.created_at).seconds // 3600

    def __str__(self):
        # used to print out the tweet object
        return f'{self.created_at} {self.user}: {self.content}'
