from django.db import models

# Create your models here.

class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='') # To add a column default value is required.cd
	list = models.ForeignKey(List, default=None)


