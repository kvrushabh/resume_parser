from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    auth_token= models.CharField(max_length=100)
    forgot_password_token= models.CharField(max_length=100)
    is_verified= models.BooleanField(default=False)
    otp= models.CharField(max_length=10, default=000000)
    created_at= models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username


