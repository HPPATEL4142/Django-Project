from rest_framework import status
from rest_framework.response import Response
from django.http import Http404 
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password

# Create your views here.

class Userview(viewsets.ViewSet):
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"error": False , "statusCode":201,"message":"Successfully user created" }, status=201)

            else:
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
            
        except Exception as e:
            print('Userview create error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"Something went wrong" }, status=422)
    
    def update(self, request, pk=None):
        try:
            queryset = User.objects.get(pk=pk)
            serializer = UserSerializer(queryset, data=request.data,partial=True)
            if serializer.is_valid():
                if serializer.validated_data.get('password') != None:
                    serializer.save(password = make_password(serializer.validated_data['password']))
                else:
                    serializer.save()
                return JsonResponse({"error": False , "statusCode":200,"message":"Successfully user updated" }, status=200)

            else:
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
        except User.DoesNotExist as e:
            print('Userview update error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"User not found" }, status=422)
        
    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return JsonResponse({"error": False , "statusCode":200,"message":"Successfully user deleted" }, status=200)
        except User.DoesNotExist as e:
            return JsonResponse({"error": True , "statusCode":422,"message":"User not found" }, status=422)

class Blogview(viewsets.ViewSet):
    def list(self, request):
        queryset = Blog.objects.all()
        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)
        
    def create(self, request):
        try:
            serializer = BlogSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"error": False , "statusCode":201,"message":"Successfully blog created" }, status=201)

            else:
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
            
        except Exception as e:
            print('Blogview create error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"Something went wrong" }, status=422)

    def update(self, request, pk=None):
        try:
            queryset = Blog.objects.get(pk=pk)
            serializer = BlogSerializer(queryset, data=request.data,partial=True)
            if serializer.is_valid():
                if request.data.get('user_id') == queryset.user_id_id:
                    serializer.save()
                    return JsonResponse({"error": False , "statusCode":200,"message":"Successfully blog updated" }, status=200)
                else:
                    return JsonResponse({"error": False , "statusCode":403,"message":"Permission denied" }, status=403)
                
            else:       
                
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
            
        except Blog.DoesNotExist as e:
            print('Blogview update error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"Blog not found" }, status=422)

    def destroy(self, request, pk=None):
        try:
            queryset = Blog.objects.get(pk=pk)
            if request.data.get('user_id') == queryset.user_id_id:
                queryset.delete()
                return JsonResponse({"error": False , "statusCode":200,"message":"Successfully blog deleted" }, status=200)

            else:
                return JsonResponse({"error": False , "statusCode":403,"message":"Permission denied" }, status=403)
      
        except Blog.DoesNotExist as e:
            return JsonResponse({"error": True , "statusCode":422,"message":"Blog not found" }, status=422)
        

class Likeview(viewsets.ViewSet):
    def list(self, request):
        queryset = Like.objects.all()
        serializer = LikeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            serializer = LikeSerializer(data=request.data)
            if serializer.is_valid():
                like_data = list(Like.objects.filter(user_id_id = request.data.get('user_id'),blog_id_id = request.data.get('blog_id')))
                if like_data == []:
                    serializer.save()
                return JsonResponse({"error": False , "statusCode":201,"message":"Successfully like updated" }, status=201)

            else:       
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
            
        except Exception as e:
            print('LikeViewSet create error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"Something went wrong" }, status=422)
        
    def update(self, request, pk=None):
        try:
            queryset = Like.objects.get(pk=pk)
            serializer = LikeSerializer(queryset, data=request.data,partial=True)
            if serializer.is_valid():
                like_data = list(Like.objects.filter(user_id_id = request.data.get('user_id'),blog_id_id = request.data.get('blog_id')))
                if like_data == []:
                    serializer.save()
                else:
                    return JsonResponse({"error": True , "statusCode":422,"message":"This user already like this blog." }, status=422)
                return JsonResponse({"error": False , "statusCode":200,"message":"Successfully like updated" }, status=200)

            else:       
                
                error_dic ={}
                response_obj = {
                    "error":True,
                    "statusCode":422,
                    "errors":error_dic
                }
                for error in serializer.errors:
                    error_dic[error] = serializer.errors[error][0]
                return Response(response_obj, status=422)
            
        except Like.DoesNotExist as e:
            print('LikeViewSet update error',e)
            return JsonResponse({"error": True , "statusCode":422,"message":"Like not found" }, status=422)


    def destroy(self, request, pk=None):
        try:
            queryset = Like.objects.get(pk=pk)
            queryset.delete()
            return JsonResponse({"error": False , "statusCode":200,"message":"Successfully like deleted" }, status=200)

        except Like.DoesNotExist as e:
            return JsonResponse({"error": True , "statusCode":422,"message":"Like not found" }, status=422)