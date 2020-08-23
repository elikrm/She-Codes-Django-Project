from django.db import models

class NewsStory(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    content = models.TextField()
    image_url = models.CharField(max_length=200, default ="https://api.time.com/wp-content/uploads/2019/03/us-movie-rabbits-meaning.jpg") 
    
