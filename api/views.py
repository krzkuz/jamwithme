from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import PostSerializer
from posts.models import Post


@api_view(['GET'])
def get_routes(request):
    routes = [
        {'GET':'/api/posts'},
        {'GET':'/api/posts/id'},
        {'POST':'/api/posts/id/rate'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    return Response(routes)

@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_post(request, pk):
    post = Post.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_vote(request, pk):
    post = Post.objects.get(id=pk)
    profile = request.user.profile
    data = request.data
    if data['vote'] == 'like':
        post.likes.add(profile)
    elif data['vote'] == 'dislike':
        post.dislikes.add(profile)
    post.save()
    print('DATA:', data)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)