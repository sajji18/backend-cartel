# from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from .models import Feature
from .serializer import FeatureSerializer
from rest_framework import status

from authentication.models import User

# class SavedPostsView(generics.ListAPIView):
#     queryset = Feature.objects.all()
#     serializer_class = FeatureSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     saved_posts = [feature.saved_posts.split(',') for feature in queryset if feature.saved_posts]
    #     # Flatten the list of saved posts
    #     saved_posts = [int(post_id) for sublist in saved_posts for post_id in sublist]
    #     return Response(saved_posts)

class SavedPostsView(generics.ListAPIView):
    serializer_class = FeatureSerializer

    def get_queryset(self):
        # username = self.request.query_params.get('username', None)
        # print(username)
        
        username = self.kwargs.get('username')

        if username:
            queryset = Feature.objects.filter(username=username)
        else:
            queryset = Feature.objects.all()

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serialized_data = self.serializer_class(queryset, many=True).data

        return Response(serialized_data)





class AddToSavedPostsView(generics.UpdateAPIView):
    serializer_class = FeatureSerializer

    def update(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = User.objects.filter(username=username, user_type='user').first()  # Assuming 'user_type' exists in the User model
        if not user:
            return Response("User not found or doesn't have the necessary permissions", status=status.HTTP_401_UNAUTHORIZED)

        feature = Feature.objects.filter(username=username).first()
        if not feature:
            feature = Feature(username=username)  # If the user's feature record doesn't exist, create a new one

        post_id = request.data.get('post_id')
        if post_id:
            if feature.saved_posts:
                feature.saved_posts += f',{post_id}'
            else:
                feature.saved_posts = post_id
            feature.save()
            return Response("Post added to saved posts", status=status.HTTP_200_OK)
        else:
            return Response("Post ID is required", status=status.HTTP_400_BAD_REQUEST)

class RegisterToEventView(generics.UpdateAPIView):
    serializer_class = FeatureSerializer

    def update(self, request, *args, **kwargs):
        username = request.data.get('username')
        user = User.objects.filter(username=username, user_type='user').first()  # Assuming 'user_type' exists in the User model
        if not user:
            return Response("User not found or doesn't have the necessary permissions", status=status.HTTP_401_UNAUTHORIZED)

        feature = Feature.objects.filter(username=username).first()
        if not feature:
            feature = Feature(username=username)  # If the user's feature record doesn't exist, create a new one

        event_name = request.data.get('event_name')
        if event_name:
            if feature.registered_events:
                feature.registered_events += f',{event_name}'
            else:
                feature.registered_events = event_name
            feature.save()
            return Response("Event registered", status=status.HTTP_200_OK)
        else:
            return Response("Event name is required", status=status.HTTP_400_BAD_REQUEST)