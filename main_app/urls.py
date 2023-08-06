from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('token/', Token.as_view(), name='token'),
    path('data/', DataApiView.as_view(), name='post-data'),
    path('data/<str:key>/', DataControlView.as_view(), name='get-data'),
    path('data/<str:key>/', DataControlView.as_view(), name='update-data'),
    path('tokdataen/<str:key>/', DataControlView.as_view(), name='delete-data'),

]