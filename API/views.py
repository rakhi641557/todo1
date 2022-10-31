from re import T
from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from API.models import Todos
from API.serializers import RegistrationSerializer, TodoSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework import authentication,permissions
# Create your views here.

class TodoView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    def retrieve(self,request,*args,**kw):
        id=kw.get("pw")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs,manay=False)
        return Response(data=serializer.data)
    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="deleted")
    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


#localhost:8000/api/v1/todos/pending_todos/
#get
#localhost:8000/api/todos/completed_todos/
#get

class TodoModelViews(ModelViewSet):
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    
    serializer_class=TodoSerializer
    queryset=Todos.objects.all()

    def get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

    # def perform_create(self, serializer):
    #     return serializer.save(user=self.request.user)

    # def list(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)
        
#action koduthekanadhu decorators aahnu prgm endhelum add cheyyanenki decorator kodukanum
   
    @action(methods=['GET'],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=['GET'],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)
   
    @action(methods=['POST'],detail=True)
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        # Todos.objects.filter(id=id).update(status=False)
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=True)
        return Response(data=serializer.data)

class UserView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()

    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors) 

     