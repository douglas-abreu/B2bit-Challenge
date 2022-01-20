from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import models
from . import serializers


class PublicationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        current_user = request.user
        queryset = models.Publication.objects.select_related('usercustom').filter(
        id__isnull=False, 
        usercustom__id__isnull=False).exclude(usercustom=current_user.id).order_by('-id')[:10]
        serializer = serializers.PublicationSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        current_user = request.user
        serializer = serializers.PublicationSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            publication = models.Publication()
            user = models.User()
            publication.usercustom = user.objects.get(pk=data.request.get('usercustom'))
            publication.title = request.data.title
            publication.content = request.data.content
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
