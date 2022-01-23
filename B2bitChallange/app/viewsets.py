from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from . import models
from . import serializers
from app.models import User


class PublicationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PublicationSerializer

    def list(self, request):
        current_user = request.user
        #queryset = models.Publication.objects.select_related(
        #    'usercustom').exclude(usercustom=current_user.id).order_by('-id').values(
        #        'usercustom__email', 'title', 'content')[:10]
        queryset = models.Publication.objects.exclude(
            usercustom=current_user.id).order_by('-id')[:10]
        print(queryset.query)
        serializer = serializers.PublicationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        current_user = request.user
        serializer = serializers.PublicationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            publication = models.Publication()
            publication.usercustom = User.objects.get(pk=current_user.id)
            publication.title = request.data['title']
            publication.content = request.data['content']
            publication.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    
    def create(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User()
            user.email = request.data['email']
            user.set_password(request.data['password'])
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

