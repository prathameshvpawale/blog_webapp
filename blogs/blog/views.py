from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import Post
from django.views.generic import (
ListView,
DetailView,
CreateView,
UpdateView,
DeleteView,)
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
import os
import uuid
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Comment
from .forms import CommentForm
# Create your views here.

def home(request):
    context = {
    'posts':Post.objects.all()   
    }
    return render(request,'blog/home.html',context=context)


def about(request):
    """Simple about page view."""
    return render(request, 'blog/about.html')


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # provide an empty comment form so the template can render it
        context['form'] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content','image','thumbnail']


    def form_valid(self, form):
        form.instance.author = self.request.user
        # ensure uploaded file is assigned explicitly
        if self.request.FILES.get('image'):
            form.instance.image = self.request.FILES.get('image')
        if self.request.FILES.get('thumbnail'):
            form.instance.thumbnail = self.request.FILES.get('thumbnail')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content','image','thumbnail']


    def form_valid(self, form):
        form.instance.author = self.request.user
        # ensure uploaded file is assigned explicitly on update as well
        if self.request.FILES.get('image'):
            form.instance.image = self.request.FILES.get('image')
        if self.request.FILES.get('thumbnail'):
            form.instance.thumbnail = self.request.FILES.get('thumbnail')
        return super().form_valid(form)
    

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def delete(self,*args,**kwargs):
        messages.success(self.request,"Post deleted successfully.")
        return super().delete(self,kwargs["pk"]) 

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user


def froala_image_upload(request):
    """Custom Froala image upload handler.

    Saves uploaded images under MEDIA_ROOT/blog_pics/<username>/post_<id>/images/
    Accepts optional `post_id` in POST to place under that post folder.
    Returns JSON with `link` field required by Froala.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    upload = request.FILES.get('file') or request.FILES.get('image')
    if not upload:
        return HttpResponseBadRequest('No file uploaded')

    username = request.user.username if request.user.is_authenticated else 'anonymous'
    post_id = request.POST.get('post_id') or request.POST.get('post')
    if post_id:
        post_segment = f"post_{post_id}"
    else:
        post_segment = f"new_{timezone.now().strftime('%Y%m%d%H%M%S')}"

    subdir = os.path.join('blog_pics', username, post_segment, 'images')
    full_dir = os.path.join(settings.MEDIA_ROOT, subdir)
    os.makedirs(full_dir, exist_ok=True)

    ext = os.path.splitext(upload.name)[1]
    filename = f"{uuid.uuid4().hex}{ext}"
    # Use posix-style path for URLs
    relative_path = '/'.join([subdir.replace('\\','/'), filename])
    save_path = os.path.join(settings.MEDIA_ROOT, subdir, filename)

    with open(save_path, 'wb+') as dest:
        for chunk in upload.chunks():
            dest.write(chunk)

    link = settings.MEDIA_URL.rstrip('/') + '/' + relative_path
    return JsonResponse({'link': link})


@login_required
def add_comment(request, pk):
    """Create a comment for post with primary key `pk`. User must be logged in."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post-detail', pk=pk)
    return redirect('blog:post-detail', pk=pk)


@login_required
def delete_comment(request, post_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, post__pk=post_pk)
    post = comment.post
    # Allow deletion by comment author or post owner
    if request.user == comment.author or request.user == post.author:
        comment.delete()
        messages.success(request, 'Comment deleted')
    else:
        messages.error(request, 'You do not have permission to delete this comment')
    return redirect('blog:post-detail', pk=post_pk)

