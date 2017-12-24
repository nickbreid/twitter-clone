from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from tweets.models import Tweet
from .serializers import TweetModelSerializer
from .pagination import StandardResultsPagination

class LikeToggleAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk, format=None):
        tweet_qs = Tweet.objects.filter(pk=pk)
        message = "You must be logged in to like a tweet."
        if request.user.is_authenticated():
            is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
            return Response({"liked": is_liked})
        return Response({"message": message}, status=400)

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

    def get_serializer_context(self, *args, **kwargs):
        context = super(TweetListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):

        requested_user = self.kwargs.get("username")

        if requested_user:
            # requested_user_follows = self.request.user.profile.get_following()
            # followed_user_tweets = Tweet.objects.filter(user__in=requested_user_follows)
            requested_user_tweets = Tweet.objects.filter(user__username=requested_user).order_by(
            "-timestamp")
            qs = requested_user_tweets

        else:
            this_user_follows = self.request.user.profile.get_following()
            followed_user_tweets = Tweet.objects.filter(user__in=this_user_follows)
            user_own_tweets = Tweet.objects.filter(user=self.request.user)
            qs = (followed_user_tweets | user_own_tweets ).distinct().order_by("-timestamp")

        query = self.request.GET.get("q", None)

        if query is not None:
            qs = qs.filter(
            Q(content__icontains=query) |
            Q(user__username__icontains=query)
            )
        return qs
