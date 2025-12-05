from django.shortcuts import render
from ConferenceApp.forms import ConferenceModel
from ConferenceApp.models import conference, submission
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def all_conferences(req):
    conferences = conference.objects.all()
    return render(req, 'conference/liste.html', {'liste': conferences})

def filter_conferences(request):
    theme = request.GET.get('theme')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')
    conferences = conference.objects.all()
    if theme:
        conferences = conferences.filter(theme=theme)
    if start and end:
        conferences = conferences.filter(start_date__gte=start, end_date__lte=end)
    return render(request, 'conference/liste.html', {'liste': conferences})

class ConferenceList(ListView):
    model = conference
    context_object_name = 'liste'
    ordering = ['start_date']
    template_name = 'conference/liste.html'
class ConferenceDetail(DetailView):
    model = conference
    template_name = 'conference/detail.html'
    context_object_name = 'conference'
class ConferenceCreate(LoginRequiredMixin,CreateView):
    model=conference
    template_name="conference/conference_form.html"
   # fields="__all__"
    success_url=reverse_lazy("conference_liste")
    form_class=ConferenceModel

class ConferenceUpdate(LoginRequiredMixin,UpdateView):
    model=conference
    template_name="conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")
class ConferenceDelete(LoginRequiredMixin,DeleteView):
     model=conference
     template_name="conference/conference_confirm_delete.html"
     success_url=reverse_lazy("conference_liste")

class SubmissionDetail(DetailView):
    model = submission
    template_name = 'conference/submission_detail.html'
    context_object_name = 'submission'


class SubmissionList(LoginRequiredMixin, ListView):
    model = submission
    template_name = 'conference/submission_list.html'
    context_object_name = 'submissions'
    paginate_by = 20

    def get_queryset(self):
        # Filter submissions by conference PK from URL and by the logged-in user
        conference_pk = self.kwargs.get('conference_pk')
        qs = submission.objects.filter(user_id=self.request.user)
        if conference_pk is not None:
            qs = qs.filter(conference__pk=conference_pk)
        return qs.order_by('-submission_date')

class SubmissionCreate(LoginRequiredMixin, CreateView):
    model = submission
    template_name = 'conference/submission_form.html'
    # let user provide an id, but set user and conference automatically
    fields = ['submission_id', 'title', 'abstract', 'key_words', 'paper', 'status', 'payed']

    def dispatch(self, request, *args, **kwargs):
        # Ensure the conference exists (will raise 404 if not)
        from django.shortcuts import get_object_or_404
        self.conference = get_object_or_404(conference, pk=self.kwargs.get('conference_pk'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # set the author and conference before saving
        form.instance.user_id = self.request.user
        form.instance.conference = self.conference
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('submission_list', kwargs={'conference_pk': self.conference.pk})


class SubmissionUpdate(LoginRequiredMixin, UpdateView):
    model = submission
    template_name = 'conference/submission_form.html'
    fields = ['title', 'abstract', 'key_words', 'paper']

    def get_queryset(self):
        # Only allow owners to edit
        return submission.objects.filter(user_id=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        # Prevent editing if accepted or rejected
        if obj.status in ['accepted', 'rejected']:
            raise PermissionDenied("This submission cannot be modified.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Ensure immutable fields are not changed by the form (they are not in fields list)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the submission list for the conference
        return reverse_lazy('submission_list', kwargs={'conference_pk': self.object.conference.pk})




