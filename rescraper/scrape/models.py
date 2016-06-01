from django.db import models

class Property(models.Model):
    address = models.CharField(max_length=400)
    external_identifier = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(decimal_places=0, max_digits=7, blank=True)
    features = models.CharField(max_length=400, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    detail_url = models.URLField(blank=True)
    is_multifamily = models.BooleanField()
    is_commercial = models.BooleanField()
    is_auction = models.BooleanField()
    date_listed = models.DateField()
    auction_date = models.DateField(blank=True)
    notes = models.CharField(max_length=500, blank=True)
    assessor_url = models.URLField(blank=True)
    tax_url = models.URLField(blank=True)
    google_map_url = models.URLField(blank=True)
    price_per_foot = models.DecimalField(decimal_places=2,  max_digits=5, blank=True, null=True)

    def __str__(self):
        return self.address

    class Meta:
        ordering = ["date_listed"]
        verbose_name_plural = "Properties"


