from django.db import models
from datetime import datetime

class Property(models.Model):
    address = models.CharField(max_length=400)
    external_identifier = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(decimal_places=0, max_digits=7, blank=True, null=True)
    features = models.CharField(max_length=400, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    detail_url = models.URLField(blank=True, null=True)
    is_multifamily = models.BooleanField(default=False)
    is_commercial = models.BooleanField(default=False)
    is_auction = models.BooleanField(default=False)
    date_listed = models.DateField(default=datetime.now())
    auction_date = models.DateField(blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True)
    assessor_url = models.URLField(blank=True, null=True)
    tax_url = models.URLField(blank=True, null=True)
    google_map_url = models.URLField(blank=True, null=True)
    price_per_foot = models.DecimalField(decimal_places=2,  max_digits=5, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ["date_listed"]
        verbose_name_plural = "Properties"


