from django.db import models
import uuid
# Create your models here.

class QuoteModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  quote = models.TextField()
  quote_by = models.CharField(max_length=200, default='Praveen Vishwakarma', null=True)
  def __str__(self):
    return self.quote