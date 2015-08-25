from django.db import models

# Create your models here.
class Restaurant(models.Model):
	business_id = models.CharField(max_length=200)
	name = models.CharField(max_length=200)
	full_address = models.CharField(max_length=300)
	city = models.CharField(max_length=200)
	state = models.CharField(max_length=200)
	stars = models.CharField(max_length=200)
	longitude = models.CharField(max_length=200)
	latitude = models.CharField(max_length=200)