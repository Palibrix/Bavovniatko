from django.db import models


class Drone(models.Model):
    frame = models.ForeignKey('components.Frame', on_delete=models.SET_NULL, null=True)
