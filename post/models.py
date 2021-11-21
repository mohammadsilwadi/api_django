from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.
class Snack(models.Model):
    title =models.CharField(max_length=256)
    purchaser=models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True, null=True)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("snack_detail",args=[str(self.id)])
