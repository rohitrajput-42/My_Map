from django.db import models

class Measurement(models.Model):
    location = models.CharField(max_length = 200)
    destination = models.CharField(max_length = 200)
    distance = models.DecimalField(max_digits = 10, decimal_places = 2)
    created = models.DateTimeField(auto_now_add = True)
    created_by = models.CharField(max_length = 200)

    def __str__(self):
        return f"The distance between {self.location} and {self.destination} is: {self.distance} Kms."