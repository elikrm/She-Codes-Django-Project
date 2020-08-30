from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.StoryView.as_view(), name='story'),
    path('add-story/', views.AddStoryView.as_view(), name='newStory'),
    path('serach-view/', views.SearchView.as_view(), name='searchStory'),
    path('<int:pk>/update-story/',views.ViewUpdateStory.as_view(), name ='updateStory'),
    path('<int:pk>/delete-story/',views.ViewDeletePost.as_view(), name ='deleteStory'),
]
