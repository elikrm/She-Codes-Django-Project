from django.views import generic
from django.urls import reverse_lazy
from .models import NewsStory
from .forms import StoryForm
from itertools import chain
from users.models import CustomUser

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

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

    # def success(self):
    #     request = self.request
    #     return HttpResponse('successfully uploaded')    

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

class ViewDeleteStory(generic.DeleteView):
    template_name = 'news/delete.html'
    model = NewsStory
    # Notice get_success_url is defined here and not in the model, because the model will be deleted
    def get_success_url(self):
        return reverse('news:index')

class AdvancedSearchView(generic.ListView):
    model = NewsStory
    template_name = 'news/Advancedsearch.html'
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
            NewsStory_results        = NewsStory.objects.Advancedsearch(query)
            
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

class SimpleSearchView(generic.ListView):
    model = NewsStory
    template_name = 'news/Simplesearch.html'

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q')

        if query:
            results = NewsStory.objects.filter(Q(category_story__icontains = query) | Q(title__icontains = query))
            # combine querysets 
            queryset_chain = chain(
                    results,
            )      
            qs = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        else:
            results = NewsStory.objects.all()

        # pages = Paginator(request, results, num =1)
        # contex = {
        #     'item': pages[0],
        #     'page-range': pages[1]
        # }
        return results