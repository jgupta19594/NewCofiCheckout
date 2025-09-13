from django.db import models

class Product(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name

