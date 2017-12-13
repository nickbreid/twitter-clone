from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsPagination

class RetweetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = "Not allowed"
        if tweet_qs.exists() and tweet_qs.count() == 1:
            #if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet_qs.first())
            if new_tweet is not None:
                data = TweetModelSerializer(new_tweet).data
                return Response(data)
            message = "Cannot retweet the same in 1 day"
        return Response({"message": message}, status=400)

class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class TweetListAPIView(generics.ListAPIView):

    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        users_followed = self.request.user.profile.get_following()
        followed_user_tweets = Tweet.objects.filter(user__in=users_followed)
        user_own_tweets = Tweet.objects.filter(user=self.request.user)
        query = self.request.GET.get("q", None)
        qs = (followed_user_tweets | user_own_tweets ).distinct().order_by(
        "-timestamp"
        )
        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs
