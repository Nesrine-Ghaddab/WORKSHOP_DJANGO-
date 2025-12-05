from django.shortcuts import render
from  SessionApp.models import Session
from SessionAppApi.serializers import SessionSerializer
from rest_framework import viewsets

class SessionViewSet(viewsets.ModelViewSet):

    queryset = Session.objects.all()
    serializer_class = SessionSerializer