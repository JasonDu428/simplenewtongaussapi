from django.db import models

# Create your models here.
class Production(models.Model):
    production_list = models.CommaSeparatedIntegerField(max_length=999999)
    def __str__(self):
        return self.production_list