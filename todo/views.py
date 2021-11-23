from . models import Task
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError


# Create your views here.
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(methods=["POST"], request_body=TaskSerializer())
@api_view(["GET", "POST"])
def task(request):
    if request.method == "GET":
        all_tasks = Task.objects.all()
        serializer = TaskSerializer(all_tasks, many=True)

        data = {
            "message" : "Success",
            "data" : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            data = {
                "message" : "Success",
                "data" : serializer.data
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message" : "Failed",
                "errors" : serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=["PUT", "DELETE"], request_body=TaskSerializer())
@api_view(["GET", "PUT", "DELETE"])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id = task_id) ## get the data from the model
    except Task.DoesNotExist:
        error = {
                "message" : "Failed",
                "errors" : f"Student with id {task_id} does not exist."
            }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        serializer = TaskSerializer(task)
        data = {
            "message" : "Success",
            "data" : serializer.data
        }  #prepare the response data

        return Response(data, status = status.HTTP_200_OK) ## Send the response.

    elif request.method == "PUT":
        serializer = TaskSerializer(task, data=request.data, partial = True)

        if serializer.is_valid():
            serializer.save()
            serializer = TaskSerializer(task)
            data = {
                "message" : "Success",
                "data" : serializer.data
            }  #prepare the response data

            return Response(data, status = status.HTTP_202_ACCEPTED)

        else:
            error = {
                "message" : "Failed",
                "data" : serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE": 
        task.delete()

        return Response({"message":"Success"}, status=status.HTTP_204_NO_CONTENT)