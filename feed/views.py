from rest_framework import generics, permissions, status
from .models import Post
from .serializers import PostSerializer
from authentication.models import User
from rest_framework.response import Response

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

# PostCreate working => only clubs can create, users cannot. Media is stored as url 
class PostCreate(generics.CreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        current_user = self.request.user # Get the current user
        if current_user.user_type == 'club' or current_user.user_type == 'Club':
            serializer = PostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        
        return Response("Forbidden: Only users with user_type='club' can create posts.", status=status.HTTP_403_FORBIDDEN)
