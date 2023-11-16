from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
<<<<<<< Updated upstream
    name = models.CharField(null=True, blank=True, max_length=60)


=======
    name = models.CharField(null=True, blank=True, max_length=60)
>>>>>>> Stashed changes
