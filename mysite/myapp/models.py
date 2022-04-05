from django.db import models
import uuid
# Create your models here.

class UserSignupModel(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=200)
    user_email = models.EmailField(unique=True)
    user_account = models.CharField(max_length=200)
    user_isfc_code = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)