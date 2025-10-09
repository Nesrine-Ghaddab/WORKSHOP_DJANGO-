from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.

import uuid
def generate_user_id():
    return "User"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domain = ["esprit.tn", "gmail.com", "yahoo.com", "outlook.com"]
    if email.split('@')[1] not in domain:
       raise ValidationError("Email domain not allowed.")

name_validator=RegexValidator(
    regex=r'^[a-zA-Z]+$',
    message='This field should contain only alphabetic characters.'
)
class User(AbstractUser):
    user_id=models.CharField(max_length=8, primary_key=True,unique=True,editable=False)
    first_name = models.CharField(max_length=100, validators=[name_validator])
    last_name = models.CharField(max_length=100, validators=[name_validator])
    email = models.EmailField(unique=True,validators=[verify_email])
    affiliation = models.CharField(max_length=255)
    nationality= models.CharField(max_length=255)
    role=[
        ('participant', 'Participant'),
        ('organisateur', 'membre commite organisateur'),

    ]
    role = models.CharField(max_length=255, choices=role, default='participant')     
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #submissions=models.ManyToManyField('ConferenceApp.submission', through='ConferenceApp.submission')
    #organizing_comitee = models.ManyToManyField('ConferenceApp.conference',through='UserApp.organizing_comitee')
    def save(self, *args, **kwargs):
        if not self.user_id:
            new_id = generate_user_id()
            while User.objects.filter(user_id=new_id).exists():
                new_id = generate_user_id()
            self.user_id = new_id
        super().save(*args, **kwargs)


class organizing_comitee(models.Model):
        comitee_id=models.AutoField(primary_key=True)
        user_id=models.ForeignKey('UserApp.User',
                                   on_delete=models.CASCADE,
                                   related_name="committees")
        conference_id=models.ForeignKey('ConferenceApp.conference', 
                                        on_delete=models.CASCADE,
                                        related_name="committees")
        role_in_comitee=models.CharField(max_length=255)
        roles=[
              ('chair', 'Chair'),
              ('co-chair', 'Co-Chair'), 
              ('member', 'Member'),
       ]    
        role_in_comitee=models.CharField(max_length=255, choices=roles)
        date_join=models.DateField()

        created_at=models.DateTimeField(auto_now_add=True)  
        updated_at=models.DateTimeField(auto_now=True)