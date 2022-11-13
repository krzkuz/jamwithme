from rest_framework import serializers
from posts.models import Post, Tag, Comment
from users.models import Profile


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(many=False)
    likes = ProfileSerializer(many=True)
    dislikes = ProfileSerializer(many=True)
    tags = TagSerializer(many=True)
    comments = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = '__all__'

    def get_comments(self, obj):
        comments = obj.comment_set.all()
        serializer = CommentSerializer(comments, many=True)
        return serializer.data