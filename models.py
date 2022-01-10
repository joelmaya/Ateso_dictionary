from django.db import models

# Create your models here.

class item(models.Model):
	word = models.CharField(max_length=255)
	translate = models.TextField()

	def __str__(self):
		return self.word

