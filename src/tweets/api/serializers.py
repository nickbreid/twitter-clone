from rest_framework import serializers
from accounts.api.serializers import UserDisplaySerializer
from tweets.models import Tweet # from ..models import Tweet
from django.utils.timesince import timesince

class ParentTweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'timestamp',
            'date_display',
            'time_since',
            'id',
            'likes',
            'did_like',

        ]

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.liked.all():
                return True
        return False


    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_time_since(self, obj):
        return timesince(obj.timestamp) + " ago"


class TweetModelSerializer(serializers.ModelSerializer):
    parent_id = serializers.CharField(write_only=True, required=False)
    user = UserDisplaySerializer(read_only=True)
    date_display = serializers.SerializerMethodField()
    time_since = serializers.SerializerMethodField()
    parent = ParentTweetModelSerializer(read_only=True)
    likes = serializers.SerializerMethodField()
    did_like = serializers.SerializerMethodField()


    class Meta:
        model = Tweet
        fields = [
            'user',
            'content',
            'timestamp',
            'date_display',
            'time_since',
            'id',
            'parent',
            'likes',
            'did_like',
            'reply',
            'parent_id',

        ]
        # read_only_fields = ['reply']

    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated():
            if user in obj.liked.all():
                return True
        return False

    def get_likes(self, obj):
        return obj.liked.all().count()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_time_since(self, obj):
        return timesince(obj.timestamp) + " ago"
