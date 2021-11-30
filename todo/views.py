from . models import Task
from .serializers import TaskSerializer, FutureSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone


# Create your views here.
@swagger_auto_schema(methods=["POST"], request_body=TaskSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["GET", "POST"])
def task(request):
    if request.method == "GET":
        all_tasks = Task.objects.filter(author=request.user)
        serializer = TaskSerializer(all_tasks, many=True)

        data = {
            "message" : "Success",
            "data" : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')

            object = Task.objects.create(**serializer.validated_data, author=request.user)
            serializer = TaskSerializer(object)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message" : "Failed",
                "errors" : serializer.errors
            }

            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=["PUT", "DELETE"], request_body=TaskSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(["GET", "PUT", "DELETE"])
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id = task_id) ## get the data from the model
    except Task.DoesNotExist:
        error = {
                "message" : "Failed",
                "errors" : f"Student with id {task_id} does not exist."
            }

        return Response(error, status=status.HTTP_404_NOT_FOUND)

    if task.user != request.user:
        raise PermissionDenied(detail="You do not have permission to perform this action")

    if request.method == "GET":
        if task.completed == False:
            task.completed=True
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



@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def mark_complete(request, todo_id):

    try:
        obj = Task.objects.get(id = todo_id)

    except Task.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user != request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')


    if request.method == 'GET':
        if obj.completed == False:
            obj.completed=True
            obj.save()

            data = {
                    'status'  : True,
                    'message' : "Successful"
                }

            return Response(data, status=status.HTTP_200_OK)
        else:

            data = {
                    'status'  : False,
                    'message' : "Already marked complete"
                }

            return Response(data, status=status.HTTP_400_BAD_REQUEST)



@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET'])
def today_list(request):
    if request.method == 'GET':
        today_date = timezone.now().date()
        objects = Task.objects.filter(date=today_date, user=request.user)

        serializer = TaskSerializer(objects, many=True)
        data = {
            'status'  : True,
            'message' : "Successful",
            'data' : serializer.data,
        }

        return Response(data, status = status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=FutureSerializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def future_list(request):
    if request.method == 'POST':
        serializer = FutureSerializer(data=request.data)
        if serializer.is_valid():
            objects = Task.objects.filter(date=serializer.validated_data['date'], user=request.user)

            serializer = TaskSerializer(objects, many=True)
            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_200_OK)
        else:
            error = {
                'status'  : False,
                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(error, status = status.HTTP_200_OK)
