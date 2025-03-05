from django.urls import path 
from .views import search
urlpatterns = [
    path('api/v1/search/<str:search_query>/<int:skip>/<int:limit>', search, name="search")
]
