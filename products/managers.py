from django.db import models

class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(parent_category=None)

class SubategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(parent_category=None)