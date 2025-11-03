from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView, 
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    PostLikeView,
    FollowingFeedView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('following-feed/', FollowingFeedView.as_view(), name='following-feed'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('about/', views.about, name='blog-about'),
]