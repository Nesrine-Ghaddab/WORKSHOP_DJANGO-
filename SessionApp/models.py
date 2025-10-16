from django.db import models
from ConferenceApp.models import conference
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils import timezone
import string, random

class Session(models.Model):
    session_id = models.CharField(max_length=12, primary_key=True, editable=False)
    title = models.CharField(
        max_length=255,
        validators=[RegexValidator(
            regex=r'^[A-Za-z0-9]+$',
            message="Le nom de la salle ne doit contenir que des lettres et des chiffres."
        )]
    )
    topic = models.CharField(max_length=255)
    session_day = models.DateField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    keywords = models.CharField(max_length=255)
    submission_date = models.DateField(null=True, blank=True)
    conference = models.ForeignKey(
        'ConferenceApp.conference',
        on_delete=models.CASCADE,
        related_name="sessions",
        null=True,
        blank=True
    )
    paper = models.FileField(
        upload_to='papers/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.session_day:
            if not (self.start_time <= self.session_day <= self.end_time):
                raise ValidationError({
                    'session_day': "La date de la session doit être comprise entre la date de début et de fin de la conférence associée."
                })
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': "L'heure de fin doit être supérieure à l'heure de début."
                })
            if self.keywords:
                keywords_list = [kw.strip() for kw in self.keywords.split(',') if kw.strip()]
                if len(keywords_list) > 10:
                    raise ValidationError({
                        'keywords': "Vous ne pouvez pas dépasser 10 mots-clés."
                    })
            if self.submission_date:
                if self.session_day > self.session.start_time:
                    raise ValidationError({
                        'session_day': "La soumission ne peut être faite que pour des conférences à venir."
                    })
        # Suppression de la validation liée au participant

    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = "SUB-" + ''.join(random.choices(string.ascii_uppercase, k=8))
        super().save(*args, **kwargs)