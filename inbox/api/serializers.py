from rest_framework import serializers
from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        ##
        # example1 ： user1 关注了你
        #             actor: User1
        #             verb: 'Followed'
        # example2:  user1 给你发的帖子 tweet1 点了赞
        #            actor： user1
        #            target: tweet1
        #            verb: 给你的帖子点赞
        model = Notification
        fields = (
            'id',
            'actor_content_type',
            'actor_object_id',
            'verb',
            'action_object_content_type',
            'action_object_object_id',
            'target_content_type',
            'target_object_id',
            'timestamp',
            'unread',
        )

class NotificationSerializerForUpdate(serializers.ModelSerializer):
    # BooleanField 会自动兼容 true, false, "true", "false", "True", "1", "0"
    # 等情况，并都转换为 python 的 boolean 类型的 True / False
    unread = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ('unread',)

    def update(self, instance, validated_data):
        instance.unread = validated_data['unread']
        instance.save()
        return instance