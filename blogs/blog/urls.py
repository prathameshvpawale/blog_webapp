from django.urls import path,include
from .views import (
    home, 
    about,
    add_comment,
    delete_comment,
    PostListView, 
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView
)

app_name = 'blog'
urlpatterns = [
    path('',PostListView.as_view(),name="home"),
    path('post/<int:pk>/',PostDetailView.as_view(),name="post-detail"),
    path('post/new',PostCreateView.as_view(),name="post-create"),
    path('post/<int:pk>/update',PostUpdateView.as_view(),name="post-update"),
    path('user/<str:username>',UserPostListView.as_view(),name="user-post"),   
    path('post/<int:pk>/delete',PostDeleteView.as_view(),name="post-delete"),  
    path('about/', about, name='about'),
    path('post/<int:pk>/comment/', add_comment, name='add-comment'),
    path('post/<int:post_pk>/comment/<int:comment_pk>/delete/', delete_comment, name='delete-comment'),
    
]