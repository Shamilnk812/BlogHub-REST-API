from django.urls import path
from .views import *


urlpatterns = [
    # Endpoint to list all posts (GET) or create a new post (POST)
    path('post/', PostListCreateView.as_view(), name='post'),
    
    # Endpoint to retrieve (GET), update (PUT/PATCH), or soft-delete (DELETE) a single post by ID
    path('post/<int:id>/', PostRetrieveUpdateDestroyView.as_view(), name='post'),
]
