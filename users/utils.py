from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Profile

def paginate_profiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    left_index = (int(page) - 4)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 5)
    if right_index >paginator.num_pages:
        right_index = paginator.num_pages

    custom_range = range(left_index, right_index + 1)
    
    return custom_range, profiles

def profile_search(request, all_profiles):
    search = request.GET.get('q')
    if search:
        search_list = str(search).split()
        profiles = Profile.objects.none()
        for word in search_list:
            profiles = profiles | all_profiles.distinct().filter(
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word)  
            )
    else:
        profiles = all_profiles
        search = ''
    return profiles, search