from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/<int:seat_number>/', views.start_session, name='start_session'),
    path('end/<int:seat_number>/', views.end_session, name='end_session'),
]
