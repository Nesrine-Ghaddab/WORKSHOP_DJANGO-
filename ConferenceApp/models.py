from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    description=models.TextField(
        validators=[MinLengthValidator(limit_value=30,message="Description must be at least 30 characters long.")]
        )
    location=models.CharField(max_length=255)
    start_date=models.DateField()   
    end_date=models.DateField()
    
    THEME_CHOICES = [
        ('CS&AI', 'Computer Science and Artificial Intelligence'),
        ('CS', 'Social Science'),
        ('DS', 'Data Science'),
    ]
    theme = models.CharField(max_length=255, choices=THEME_CHOICES, default='CS&AI')
    created_at=models.DateTimeField(auto_now_add=True)  
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.end_date < self.start_date:
         raise ValidationError("End date cannot be earlier than start date.")
    

class submission(models.Model):
    submission_id=models.CharField(max_length=255, primary_key=True)
    title=models.CharField(max_length=255)
    abstract=models.TextField()
    key_words=models.TextField()
    paper=models.FileField(upload_to='papers/')
    choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'), 
        ('rejected', 'Rejected'),

    ]
    status=models.CharField(max_length=255,choices=choices, default='pending')
    payed=models.BooleanField(default=False)
    submission_date=models.DateTimeField(auto_now_add=True)
    
    user_id=models.ForeignKey('UserApp.User', on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey('conference', on_delete=models.CASCADE)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)  

    
