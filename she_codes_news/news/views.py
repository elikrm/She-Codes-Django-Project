from django.views import generic
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm
from itertools import chain
from users.models import CustomUser

from django.http import HttpResponseRedirect
from django.urls import reverse

class IndexView(generic.ListView):
    template_name = 'news/index.html'

    def get_queryset(self):
        '''Return all news stories.'''
        return NewsStory.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_stories'] = NewsStory.objects.order_by('-pub_date').all()[:4]
        context['all_stories'] = NewsStory.objects.all().order_by('-pub_date')
        return context


class StoryView(generic.DetailView):
    model = NewsStory
    template_name = 'news/story.html'
    context_object_name = 'story'
    
    # def get_user_object(self):
    #     return CustomUser.objects.all()

class AddStoryView(generic.CreateView):
    form_class = StoryForm
    context_object_name = 'storyForm'
    template_name = 'news/createStory.html'
    success_url = reverse_lazy('news:index')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)     

class SearchView(generic.ListView):
    model = NewsStory
    template_name = 'news/search.html'
    paginate_by = 20
    count = 0
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['count'] = self.count or 0
        context['query'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)
        
        if query is not None:
            NewsStory_results        = NewsStory.objects.search(query)
            
            # combine querysets 
            queryset_chain = chain(
                    NewsStory_results,
            )        
            qs = sorted(queryset_chain, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return NewsStory.objects.none() # just an empty queryset as default

class ViewUpdateStory(generic.UpdateView):
    # form_class = StoryForm
    model = NewsStory
    template_name = 'news/update.html'
    fields = ['title', 'content']
 
    def get_object(self, queryset=None):
        id = self.kwargs['pk']
        return self.model.objects.get(id=id)
        
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('news:index'))

# Display a confirmation warning before deleting, if triggered with GET: it shows the warning(template view)
# If triggered with POST then deletes, the template will receive object, which is the item to be deleted

class ViewDeletePost(generic.DeleteView):
    template_name = 'news/delete.html'
    model = NewsStory
    # Notice get_success_url is defined here and not in the model, because the model will be deleted
    def get_success_url(self):
        return reverse('news:index')