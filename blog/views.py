from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import BlogPost


# Create your views here.
class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)

        cache_key = f'blogpost_{self.object.pk}'
        cache_timeout = 60

        cached_data = cache.get(cache_key)

        if cached_data is None:
            self.object.views += 1
            self.object.save()
            cache.set(cache_key, self.object, cache_timeout)
        else:
            last_updated = timezone.now()
            time_elapsed = timezone.now() - last_updated

            if time_elapsed.total_seconds() >= cache_timeout:
                self.object.views += 1
                self.object.save()
                cache.set(cache_key, self.object, cache_timeout)

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
