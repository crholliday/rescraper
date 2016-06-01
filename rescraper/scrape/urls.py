from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views
from .views import PropertyDetail

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /scrape/5/
    url(r'^(?P<pk>[0-9]+)/*$', PropertyDetail.as_view(), name="detail"),
]

# urlpatterns += staticfiles_urlpatterns()