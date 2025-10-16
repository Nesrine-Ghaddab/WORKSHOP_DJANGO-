from django.urls import path, include
from.views import *
#from.import views
urlpatterns = [
 #   path('liste/', views.all_conferences, name='conference_liste'),
   path('liste/', ConferenceList.as_view(), name='conference_liste'),
   path('detail/<int:pk>/', ConferenceDetail.as_view(), name='conference_detail'),
]
