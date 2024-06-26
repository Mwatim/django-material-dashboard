import uuid
import datetime
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

# Create your models here.
class Country(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("apps.home:country_detail", kwargs={"name": self.name})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Country, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyTicker(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.OneToOneField('Company', on_delete=models.PROTECT)
    ticker = models.CharField(max_length=10)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("apps.home:company_detail", kwargs={"name": self.name})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyTicker, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class Company(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=350)
    origin_country = models.OneToOneField(Country, on_delete=models.PROTECT, default=1)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("apps.home:company_detail", kwargs={"ticker": CompanyTicker.objects.get(company=self).ticker})
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Company, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyFoundingYear(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    founding_year = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyFoundingYear, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyListingYear(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    listing_year = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyListingYear, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyDescription(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    description = models.TextField(max_length=1000)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyDescription, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyHeadquarters(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    headquarters = models.CharField(max_length=300)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyHeadquarters, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class Sector(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Sector, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanySector(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    sector = models.OneToOneField(Sector, on_delete=models.PROTECT, related_name='companysector')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanySector, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanyFinancialYearEnd(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.OneToOneField(Company, on_delete=models.PROTECT, related_name='companyfinancialyearend')
    financial_year_end = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(CompanyFinancialYearEnd, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)


class Subsidiary(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    parents = models.ManyToManyField(Company, through='CompanySubsidiaryRelation')
    operating_countries = models.ManyToManyField(Country, through='CountrySubsidiaryRelation')
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name='subsidiarysector')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Subsidiary, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CompanySubsidiaryRelation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.PROTECT)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(Subsidiary, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class CountrySubsidiaryRelation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subsidiary = models.ForeignKey(Subsidiary, on_delete=models.PROTECT)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(cls, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class SubsidiaryFoundingYear(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    subsidiary = models.OneToOneField(Subsidiary, on_delete=models.PROTECT, related_name='subsidiaryfoundingyear')
    founding_year = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(SubsidiaryFoundingYear, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class SubsidiaryDescription(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    subsidiary = models.OneToOneField(Subsidiary, on_delete=models.PROTECT, related_name='subsidiarydescription')
    description = models.TextField(max_length=1000)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(SubsidiaryDescription, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)

class SubsidiaryHeadquarters(models.Model):
    creator = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    subsidiary = models.OneToOneField(Subsidiary, on_delete=models.PROTECT, related_name='subsidiaryheadquarters')
    headquarters = models.CharField(max_length=300)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    edited_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_at = timezone.now()
        self.edited_at = timezone.now()
        super(SubsidiaryHeadquarters, self).save(*args, **kwargs)

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    @classmethod
    def delete(cls, *args, **kwargs):
        # Override delete method to perform soft delete and prevent hard deletion of record
        queryset = cls.objects.filter(*args, **kwargs)
        queryset.update(is_deleted=True)