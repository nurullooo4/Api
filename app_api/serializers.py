from rest_framework.serializers import ModelSerializer,SerializerMethodField
from django.contrib.auth import get_user_model

from .models import Post, Comment

User = get_user_model()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        if password:
            instance.set_password(password)
            instance.save()

        return super().update(instance, validated_data)

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class PostSerializer(ModelSerializer):
    owner = UserSerializer()
    comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        return Comment.objects.filter(post=obj).values('id', 'owner', 'body', 'created_at', 'updated_at')


class CommentSerializer(ModelSerializer):
    owner = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
