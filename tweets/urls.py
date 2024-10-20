from django.urls import path, re_path
from .views import *
from .views import register




urlpatterns = [
    path('', TweetListView.as_view(), name='list_view'),
    path('<int:pk>/',  TweetDetailView.as_view(), name='detail_view'),
    path('register/', register, name='register'),
]