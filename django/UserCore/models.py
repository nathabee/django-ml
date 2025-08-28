from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models 
from django.utils import timezone

# Table: customize User   

class CustomUser(AbstractUser):
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'Francais'),
        ('br', 'Breton'),
        ('de', 'Deutsch'),
        # Add other languages as needed
    ]
    lang = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en',  # Default to English
    )
