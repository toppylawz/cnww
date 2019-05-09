from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.utils import timezone
from django.contrib import admin
from .utils import get_unique_slug

#this filters the unpublished contents from the published ones
class ArticleFilter(models.Manager):
    def active(self, *args, **kwargs):
        return super(ArticleFilter,self).filter(draft=False).filter(publish__lte=timezone.now())


#this changes the uploaded location
def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

# Create your models here.
class Tag(models.Model):
    type = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    def __str__(self):
        return self.tag

class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    def __str__(self):
        return self.name

class Entry(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    slug=models.SlugField(max_length=50, unique=True)
    body=models.TextField(max_length=2000)
    authors = models.ManyToManyField(Author)
    draft=models.BooleanField(default=False)#controls whether content is in draft or not
    publish=models.DateField(auto_now=False, auto_now_add=False)
    image=models.ImageField(upload_to= 'static/media', default='blog.png',null=True, blank=True,
          width_field="width_field",
          height_field="height_field")
    width_field=models.IntegerField(default=0)
    height_field=models.IntegerField(default=0)
    updated= models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp= models.DateTimeField(auto_now=False, auto_now_add=True)

    objects=ArticleFilter()

    def summary(self):
        return self.body[:100]

    def __unicode__(self):
        return self.title

    def pub_date_pretty(self):
       return self.timestamp.strftime('%b %e %Y')

    #shows the content's title in the admin instead of object list
    def __str__(self):
        return self.title

    #this makes it possible for the created article to find the right path to the database
    def get_absolute_url(self):
       return reverse("articles:detail",kwargs={"slug":self.slug})
