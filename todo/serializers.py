from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "author", "completed", "created_date")


class FutureSerializer(serializers.Serializer):
    date = serializers.DateField()