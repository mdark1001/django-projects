from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

# Create a custom manager 

class PublishedManager(models.Manager):
    """ 
    A custom manager for Post published
    There are two ways to add or customize managers for your models: you can
    add extra manager methods to an existing manager, or create a new manager by
    modifying the initial QuerySet that the manager returns.
    """

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    """ Modelo que define un Post en el blog """

    STATUS = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(
        verbose_name='Título',
        max_length=250,
    )
    slug = models.SlugField(
        unique_for_date='publish',  # Create unique slugs urls using publish date
        max_length=250,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',  # reverse name relationship from User to Post.
    )
    body = models.TextField()
    publish = models.DateTimeField(
        default=timezone.now,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='draft'
    )
    # define the manager 
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])
