from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from blog.models import Post


class BlogCreateView(CreateView):
    model = Post
    fields = ('name', 'desc', 'image')
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:view')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_details.html'
    success_url = reverse_lazy('blog:view')
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Post
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy("blog:view")


class BlogUpdateView(UpdateView):
    model = Post
    fields = ('name', 'desc', 'image')
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy("blog:view")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.name)
            new_blog.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:detail', args=[self.get('pk')])


class BlogListView(ListView):
    model = Post
    fields = ('name', 'desc', 'image')
    template_name = 'blog/blog_list.html'
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)


def published_activity(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.is_published:
        post_item.is_published = False
    else:
        post_item.is_published = True
    post_item.save()
    return redirect(reverse_lazy('blog:detail', args=[post_item.pk]))
