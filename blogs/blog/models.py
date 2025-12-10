from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = FroalaField(options={
        'toolbarInline': True,
        'imageUploadURL': '/froala_editor/upload_image/',
        'imageManagerLoadURL': '/froala_editor/load_images/',
        'imageManagerDeleteURL': '/froala_editor/delete_image/',
        'imageMaxSize': 5 * 1024 * 1024,  # 5MB
    })
    image = models.ImageField(upload_to='blog_pics/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='blog_pics/thumbnails/', null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('blog:post-detail',kwargs={'pk':self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'