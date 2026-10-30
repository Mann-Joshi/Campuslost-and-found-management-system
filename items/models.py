from django.conf import settings
from django.db import models


class ItemReport(models.Model):
    LOST = 'Lost'
    FOUND = 'Found'
    ITEM_TYPES = [
        (LOST, 'Lost'),
        (FOUND, 'Found'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_type = models.CharField(max_length=5, choices=ITEM_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
