from logging import error
from os import stat
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from todo import serializers
from . models import CustomUser
from django.contrib.auth import authenticate, get_user_model
from . serializers import CustomUserSerializer, ChangePasswordSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema

User = get_user_model()

# Create your views here.
@swagger_auto_schema(methods=["POST"], request_body=CustomUserSerializer())
@api_view(["GET", "POST"])
def new_user(request):
    if request.method == "GET":
        all_user = User.objects.all()
        serializer = CustomUserSerializer(all_user, many=True)

        data = {
            "message" : "Success",
            "data" : serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data["password"] = make_password(serializer.validated_data["password"])

            user = User.objects.create(**serializer.validated_data)
            user_serializer = CustomUserSerializer(user)

            data = {
                "message" : "Success",
                "data" : user_serializer.data
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            error = {
                "message" : "Failed",
                "errors" : serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(methods=["PUT", "DELETE"], request_body=CustomUserSerializer())
@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id = user_id) ## get the data from the model
    except User.DoesNotExist:
        error = {
                "message" : "Failed",
                "errors" : f"Student with id {user_id} does not exist."
            }

        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        serializer = CustomUserSerializer(user)
        data = {
            "message" : "Success",
            "data" : serializer.data
        }  #prepare the response data

        return Response(data, status = status.HTTP_200_OK) ## Send the response.

    elif request.method == "PUT":
        serializer = CustomUserSerializer(user, data=request.data, partial = True)

        if serializer.is_valid():
            if "password" in serializer.validated_data.keys():
                raise ValidationError("Unable to change password!")
            serializer.save()
            serializer = CustomUserSerializer(user)
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
        user.delete()

        return Response({"message":"Success"}, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(methods=["POST"], request_body=LoginSerializer())
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            user = authenticate(request, username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            if user:
                if user.is_active:
                    serializer = CustomUserSerializer(user)
                    data = {
                        'message' : 'Login successful',
                        'data' : serializer.data
                    }
                    return Response(data, status=status.HTTP_200_OK)
                
                else:
                   error = {
                       'message' : 'Please activate your account'
                   }
                   return Response(error, status=status.HTTP_401_UNAUTHORIZED)
            else:
                error = {
                    'message' : 'Please enter a valid username and password'
                }
                return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        else:
            error = {
                'error' : serializer.errors
            }

            return Response(error, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    # print(user.password)
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            if check_password(old_password, user.password):

                user.set_password(serializer.validated_data['new_password'])

                user.save()

                # print(user.password)

                return Response({"message":"success"}, status=status.HTTP_200_OK)

            else:
                error = {
                'message':'failed',
                "errors":"Old password not correct"
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST) 

        else:
            error = {
                'message':'failed',
                "errors":serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)



