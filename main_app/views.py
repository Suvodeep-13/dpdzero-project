from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .serializer import *
from django.http import JsonResponse
from django.contrib.auth import get_user_model, authenticate
from django.forms.models import model_to_dict
from .models import *

# Create your views here.

class ResponseHandler:
    def handle_error_response(self, resp):
        return {"message": resp}
    
    def handle_internal_error(self):
        return {"message": "Internal Server Error", "data": None}

class Register(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                post_data = serializer.data
                if User.objects.filter(username=post_data.get('username')).exists():
                    return JsonResponse({"status": "error","code": "USERNAME_EXISTS","message": "The provided username is already taken. Please choose a different username."}, status=400)
                if User.objects.filter(email=post_data.get('email')).exists():
                    return JsonResponse({"status": "error","code": "EMAIL_EXISTS","message": "The provided email is already registered. Please use a different email address."}, status=400)
                user = User.objects.create(
                    email=post_data.get('email'),
                    username=post_data.get('username'),
                    full_name=post_data.get('full_name'),
                    gender=post_data.get('gender'),
                    age=post_data.get('age')
                )
                user.set_password(post_data.get("password"))
                user.save()
                return JsonResponse({"status":"success", "message":"User successfully registered!", "data":model_to_dict(user, fields=['id', 'username', 'email', 'full_name', 'age', 'gender'])}, status=200)
            else:
                resp = ResponseHandler().handle_error_response(serializer.errors)
                return JsonResponse(resp, status=400)
        except:
            return JsonResponse({'status':'INTERNAL_SERVER_ERROR', 'message':'An internal server error occurred. Please try again later.'}, status=500)

class Token(APIView):
    serializer_class = TokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if not user:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
            token, exp = user.generate_access_token()
            return JsonResponse({'status':'success','message': 'Access token generated successfully.',
                                 'access_token': token.decode('utf-8'),
                                 'expires_in': int(exp.timestamp())}, 
                                status=200)
        else:
            resp = ResponseHandler().handle_error_response(serializer.errors)
            return JsonResponse(resp, status=400)
        
class DataControlView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, key):
        try:
            data = Data.objects.get(key=key)
            return JsonResponse({"status": "success","data":model_to_dict(data, exclude=['id', 'user'])}, status=200)
        except Data.DoesNotExist:
            return JsonResponse({"status": "error","code": "KEY_NOT_FOUND","message": "The provided key does not exist in the database."}, status=400)
    def put(self, request, key): # update data 
        try:
            serializer = DataUpdateSerializer(data=request.data)
            if serializer.is_valid():
                data = Data.objects.get(key=key)
                data.value = request.data.get('value')
                data.save()
                return JsonResponse({"status": "success","message": "Data updated successfully."}, status=200)
            else:
                resp = ResponseHandler().handle_error_response(serializer.errors)
                return JsonResponse(resp, status=400)
        except Data.DoesNotExist:
            return JsonResponse({"status": "error","code": "KEY_NOT_FOUND","message": "The provided key does not exist in the database."}, status=400)
        
    def delete(self, request, key):
        try:
            data = Data.objects.get(key=key)
            data.delete()
            return JsonResponse({"status": "success","message": "Data deleted successfully."}, status=200)
        except Data.DoesNotExist:
            return JsonResponse({"status": "error","code": "KEY_NOT_FOUND","message": "The provided key does not exist in the database."}, status=400)
            

class DataApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request): # create data
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            if Data.objects.filter(key=request.data.get("key")).exists():
                return JsonResponse({"status": "error","code": "KEY_EXISTS","message": "The provided key already exists in the database. To update an existing key, use the update API."}, status=400)
            data = Data.objects.create(
                key = request.data.get("key"),
                value = request.data.get("value")
            )
            return JsonResponse({"status": "success","message": "Data stored successfully."}, status=200)
        else:
            resp = ResponseHandler().handle_error_response(serializer.errors)
            return JsonResponse(resp, status=400)
            
