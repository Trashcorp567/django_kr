from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogPostListView, BlogPostCreateView, BlogPostDetailView, BlogPostUpdateView, BlogPostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('blog_posts/', BlogPostListView.as_view(), name='blogpost_list'),
    path('blog_create/', BlogPostCreateView.as_view(), name='blogpost_form'),
    path('view/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('edit/<int:pk>/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('delete/<int:pk>/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]