from django.shortcuts import render
from ConferenceApp.models import conference
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView
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

class ConferenceCreate(CreateView):
    model=conference
    template_name="conference/conference_form.html"
    fields="__all__"
    success_url=reverse_lazy("conference_liste")