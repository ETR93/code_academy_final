from django.urls import path, include
from .views import Results

urlpatterns = [path("posts_results", Results.as_view())]