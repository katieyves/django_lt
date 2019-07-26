from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_list, name='hotel_list'),
    path('start', views.parse, name='parse'),
    path('filter', views.country_filter, name='country_filter'),
    path('update_info', views.update_info_view, name='update_info'),
    path('update_hotel_info', views.update_hotel_info, name='update_hotel_info')
]