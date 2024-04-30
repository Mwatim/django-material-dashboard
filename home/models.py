import uuid
import datetime
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Company(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=350)
    founding_year = models.DateTimeField()
    listing_year = models.DateTimeField()
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("apps.home:company_detail", kwargs={"name": self.name})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        self.name = str(self.start_date.year)
        super(Company, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

