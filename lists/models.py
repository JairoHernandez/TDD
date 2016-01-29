from django.db import models

# Create your models here.

class Item(models.Model):
	text = models.TextField(default='') # To add a column default value is required.

