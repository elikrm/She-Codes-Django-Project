from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q

class StoryManager(models.Manager):
    def Advancedsearch(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) | 
                         Q(category_story__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs

class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    # author = models.CharField(max_length=200)
    author = models.ForeignKey(
                                get_user_model(),
                                on_delete=models.CASCADE
                                )
    pub_date        = models.DateTimeField()
    content         = models.TextField()
    image_url       = models.CharField(max_length=200, default ="https://api.time.com/wp-content/uploads/2019/03/us-movie-rabbits-meaning.jpg") 
    category_story  = models.CharField(max_length=200, default = "Brisbane-Events")
    #main_image = models.ImageField(upload_to='images/', null=True)

    objects         = StoryManager()
    # def __str__(self):
    #  return self.author


    # def show_author(self):
    #     username = self.cleaned_data['author']

