from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost


# Create your views here.
class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostUpdateView(LoginRequiredMixin, UpdateView):
    model = BlogPost
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy('blog:blogpost_list')
