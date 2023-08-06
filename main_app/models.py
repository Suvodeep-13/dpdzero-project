from django.db import models
import jwt
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self,**data):
        """
        Create and save a User with the given email and password.
        """
        email = data.pop("email")
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        password = data.pop("password")
        user = self.model(email=email, **data)
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(**extra_fields)

class User(AbstractUser):
    full_name = models.CharField(max_length=50, null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    gender = models.CharField(max_length=15, null=False, blank=False)

    objects = CustomUserManager()

    def generate_access_token(self):
        # Generate JWT token
        exp = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_TIME)
        token_payload = {
            'user_id': self.id,
            'exp': exp
        }
        token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm='HS256')
        return token, exp
    
class Data(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='data',
    )
    key = models.CharField(max_length=255, null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)
