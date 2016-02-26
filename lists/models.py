from django.db import models

# Create your models here.

class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='') # To add a column default value is required.cd
	list = models.ForeignKey(List, default=None)


#Live on my ubuntu(no "tests")
#sqlite> select * from lists_item;
#id          text        list_id   
#----------  ----------  ----------
#1           hello       1         
