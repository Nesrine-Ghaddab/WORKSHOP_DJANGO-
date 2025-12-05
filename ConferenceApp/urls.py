from django.urls import path, include
from.views import *
from .views import filter_conferences

#from.import views
urlpatterns = [
 #   path('liste/', views.all_conferences, name='conference_liste'),
   path('liste/', ConferenceList.as_view(), name='conference_liste'),
   path('detail/<int:pk>/', ConferenceDetail.as_view(), name='conference_detail'),
    path('form/', ConferenceCreate.as_view(), name='conference_add'),
   path('<int:pk>/edit/', ConferenceUpdate.as_view(), name='conference_edit'),
   path('<int:pk>/delete/', ConferenceDelete.as_view(), name='conference_delete'),
  path('submission/<str:pk>/', SubmissionDetail.as_view(), name='submission_detail'),
  path('conference/<int:conference_pk>/submissions/', SubmissionList.as_view(), name='submission_list'),
  path('conference/<int:conference_pk>/submission/add/', SubmissionCreate.as_view(), name='submission_add'),
  path('submission/<str:pk>/edit/', SubmissionUpdate.as_view(), name='submission_edit'),
  path('conferences/filter/', filter_conferences, name='filter_conferences'),

  
]
