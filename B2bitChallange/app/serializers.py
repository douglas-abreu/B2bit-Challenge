
from rest_framework import serializers
from app.models import Publication, User


class PublicationSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Publication
        fields = ('id', 'usercustom', 'title', 'content')

    def get_message_field(self, obj):
        return obj.title

class UserSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_message_field(self, obj):
        return obj.email