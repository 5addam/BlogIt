from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Follow

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username=None):
    # Determine which user's profile is being viewed
    if username:
        profile_user = get_object_or_404(User, username=username)
    else:
        profile_user = request.user

    # Handle follow/unfollow action
    if request.method == 'POST' and 'follow_toggle' in request.POST:
        if profile_user != request.user:
            relation, created = Follow.objects.get_or_create(
                follower=request.user, following=profile_user
            )
            if not created:
                relation.delete()
            return redirect('user-profile', username=profile_user.username)

    # Handle profile update if current user is editing their own profile
    if profile_user == request.user and request.method == 'POST' and 'update_profile' in request.POST:
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    # Determine if the logged-in user is following the profile being viewed
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()

    # Count followers and following
    follower_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()

    # Paginate posts
    posts_list = profile_user.post_set.all().order_by('-date_posted')  # Replace 'post_set' with your Post model related_name
    paginator = Paginator(posts_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'profile_user': profile_user,
        'u_form': user_form,
        'p_form': profile_form,
        'is_following': is_following,
        'follower_count': follower_count,
        'following_count': following_count,
        'posts': posts,
    }

    return render(request, 'users/profile.html', context)
