from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=60)

<<<<<<< HEAD

=======
>>>>>>> b2368c7 (wiederherstellung)
