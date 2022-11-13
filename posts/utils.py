from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post, Tag

def paginate_comments(request, comments, results):
    page = request.GET.get('page')
    paginator = Paginator(comments, results)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        comments = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        comments = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index >paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    
    return custom_range, comments

def paginate_posts(request, posts, results):
    page = request.GET.get('page')
    paginator = Paginator(posts, results)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        posts = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        posts = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index >paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    
    return custom_range, posts

def post_search(request, all_posts):
    search = request.GET.get('q')
    if search:
        search_list = str(search).split()
        tags_filtered = Tag.objects.none()
        posts = Post.objects.none()
        for word in search_list:
            tags_filtered = tags_filtered | Tag.objects.filter(name=word)
        for word in search_list:
            posts = posts | all_posts.distinct().filter(
                Q(author__first_name__icontains=word) |
                Q(author__last_name__icontains=word) |
                Q(body__icontains=word) |
                Q(subject__icontains=word) |
                Q(tags__in=tags_filtered)
            )
    else:
        posts = all_posts
        search = ''
    return posts, search