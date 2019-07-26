from django.shortcuts import render
from .models import Hotel
from .lt_rooms_parser import start, update_info, update_hotel_info_parse

# Create your views here.


def hotel_list(request):
    hotels = Hotel.objects.filter(num_empty_rooms__gt=0).order_by('id_lt')
    return render(request, 'index.html', {'hotels': hotels})


def parse(request):
    if request.method == 'POST':
        start(d=request.POST.get('day'), m=request.POST.get('month'), y=request.POST.get('year'), country=request.POST.get('country'), nights=request.POST.get('nights'), stars=request.POST.get('stars'))
    hotels = Hotel.objects.filter(num_empty_rooms__gt=0).order_by('id_lt')
    return render(request, 'index.html', {'hotels': hotels})


def country_filter(request):
    hotels = Hotel.objects.filter(num_empty_rooms__gt=0).filter(country=request.GET.get('country')).order_by('id_lt')
    return render(request, 'index.html', {'hotels': hotels})


def update_info_view(request):
    update_info()
    hotels = Hotel.objects.filter(num_empty_rooms__gt=0).order_by('id_lt')
    return render(request, 'index.html', {'hotels': hotels})


def update_hotel_info(request):
    update_hotel_info_parse(id_lt=request.POST.get('id_lt'))
    hotels = Hotel.objects.filter(num_empty_rooms__gt=0).order_by('id_lt')
    return render(request, 'index.html', {'hotels': hotels})
