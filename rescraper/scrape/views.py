from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView

from .models import Property


def index(request):
    latest_property_list = Property.objects.order_by('-date_listed')[:50]
    context = {'latest_property_list': latest_property_list}
    #load_realtor_properties()
    return render(request, 'scrape/index.html', context)



class PropertyDetail(DetailView):
    model = Property
