from rest_framework import serializers
from .models import *
import re

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
    username = serializers.CharField(max_length=50, required=True, allow_blank=False)
    password = serializers.CharField(max_length=50, required=True, allow_blank=False)
    full_name = serializers.CharField(max_length=50, required=True, allow_blank=False)
    age = serializers.IntegerField(required=True)
    gender = serializers.CharField(max_length=15, required=True, allow_blank=True)

    def validate_password(self, password):
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'\d', password) or not re.search(r'[!@#$%^&*()-=_+[\]{}|;:",./<>?]', password):
            raise serializers.ValidationError({'status':'INVALID_PASSWORD','message':'The provided password does not meet the requirements. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters.'})
        return password 
    def validate_age(self, age):
        if age <= 0:
            raise serializers.ValidationError({'status':'INVALID_AGE','message':'Invalid age value. Age must be a positive integer.'})
        return age
    def validate_gender(self, gender):
        if gender not in {"male", "female", "non-binary"}:
            raise serializers.ValidationError({'status':'GENDER_REQUIRED','message':'Gender field is required. Please specify the gender (e.g., male, female, non-binary).'})
        return gender

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50, required=True, allow_blank=False)
    password = serializers.CharField(max_length=50, required=True, allow_blank=False)

class DataSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=255, required=True, allow_blank=False)
    value = serializers.CharField(max_length=255, required=True, allow_blank=False)

class DataUpdateSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=255, required=True, allow_blank=False)
    