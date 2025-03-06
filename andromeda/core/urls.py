from django.urls import path 
from .views import search, homepage
urlpatterns = [
    path('', homepage, name="homepage"),
    path('search', search, name="search")
]
