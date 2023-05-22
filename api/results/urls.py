from django.urls import path, include
from .views import Results, GetResults

urlpatterns = [path("posts_results", Results.as_view()),
               path("get_results", GetResults.as_view())]