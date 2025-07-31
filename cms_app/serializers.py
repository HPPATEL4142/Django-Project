from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'],email=validated_data['email'],name=validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class BlogSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = '__all__'
      
    def get_like_count(self, obj):
        return obj.blog.count()
    

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'