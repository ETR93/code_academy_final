from rest_framework import serializers
from .models import PostResults
from rest_framework import generics


class ResultsSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostResults
        fields = ['title']