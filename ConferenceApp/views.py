from django.shortcuts import render
from ConferenceApp.models import conference
from django.views.generic import ListView
from django.views.generic.detail import DetailView
    
# Create your views here.
def all_conferences(req):
    conferences = conference.objects.all()
    return render(req, 'conference/liste.html', {'liste': conferences})


class ConferenceList(ListView):
    model = conference
    context_object_name = 'liste'
    ordering = ['start_date']
    template_name = 'conference/liste.html'
class ConferenceDetail(DetailView):
    model = conference
    template_name = 'conference/detail.html'
    context_object_name = 'conference'