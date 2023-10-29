from django.shortcuts import redirect
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import generics
from django.http import HttpResponseRedirect
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication
from rest_framework import permissions, status
from .models import User
from .serializers import ClubLoginSerializer
from django.contrib.auth import login, logout
from .validations import validate_email, validate_password

# Create your views here.
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ClubLoginView(generics.GenericAPIView):
    serializer_class = ClubLoginSerializer
    permission_classes = (permissions.AllowAny,)
	##
    def post(self, request):
        serializer = ClubLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.check_user(request.data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



# OAUTH INTEGRATION WITH CHANNELI ###########################################################################################################


client_id = 'tEpiwYD3Vk4X3r0yPFfpkYZxavZKT8K397vyvp20'
client_secret = 'XfK9bCgPPJly5njPcHyL0EzgPLSUO5uVdAwsZoeIt9zUuqjXjWFcytfsDQ5uDn2vEikjqHRraLx3aOKuNdaXhBy5HbvJdKXA3fta5NtNRBhHXfhxD69CnoYCm13Rv4mp'
redirect_uri = 'http://127.0.0.1:8000/auth/callback/'


class OauthAuthorizeView(APIView):
    def get(self, request):
        state = 'success'
        url = f'https://channeli.in/oauth/authorise/?client_id={client_id}&redirect_uri={redirect_uri}&state={state}'
        print(url)
        return redirect(url)
    
    
class OauthCallback(APIView):
    def get(self,request):
        code = request.GET['code']
        # print(code, type(code)) 
        token_url = 'https://channeli.in/open_auth/token/'
        
        # header to be included for post request
        data = { 
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'code': code,
        }
        
        response = requests.post(token_url, data=data) # response to the post request at token_url with header = data
        response = response.json()
        
        access_token = response['access_token']
        refresh_token = response['refresh_token']
        request.session['access_token'] = access_token # storing in session
        print(request.session['access_token'])
        # print(access_token, refresh_token)
        
        user_data_url = 'https://channeli.in/open_auth/get_user_data/'
        headers = {
            'Authorization': f'Bearer {access_token}'
            }
        
        user_data = requests.get(user_data_url, headers=headers)
        
        # print(headers['Authorization'], type(headers['Authorization']))
        # print(user_data)
        
        if user_data.status_code == 200:
            user_data  = user_data.json()
            
            username = user_data['username']
            email = user_data['contactInformation']['emailAddress']
            profile_pic = user_data['person']['displayPicture']
            full_name = user_data['person']['fullName']
            words = full_name.split()
            
            current_user = User.objects.filter(username=username)
            
            if not current_user:
                new_user = User.objects.create(
                    first_name = words[0],
                    last_name = ''.join(words[1:]), # for users with name more than 2 words
                    username = username,
                    email = email,
                    profile_pic = 'https://channeli.in' + str(user_data['person']['displayPicture'])
                )
                new_user.save()
                
            else:
                existing_user = User.objects.get(username=username)
                token, created = Token.objects.get_or_create(user=existing_user)

                authToken = token.key
                userId = existing_user.user_id
                userName = existing_user.username
                
                response = HttpResponseRedirect('http://localhost:3000/home')  
                return response #Change URL to /home
        
        return redirect('http://localhost:3000/home')

class Logout(APIView):
    def get(self,request):
        print(request.session['access_token'])
        access_token = request.session['access_token']
        data={
            'client_id': client_id,
            'client_secret': client_secret,
            'token':access_token,
            'token_type_hint':'access_token'
        }
        url =' https://channeli.in/open_auth/revoke_token/'
        requests.post(url=url,data=data)
        return Response({'message': 'Logout successful'})


###############################################################################################################################################






# class CurrentUserView(APIView):
#     permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access this view

#     def get(self, request):
#         serializer = UserProfileSerializer(request.user)  # Pass the current user to the serializer
#         return Response(serializer.data)
