from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    # Placeholder URLs for future steps
    path('register/', views.register_racer, name='register_racer'),
    path('qualifying/', views.qualifying_mode, name='qualifying_mode'),
    path('race/', views.race_mode, name='race_mode'),
    path('save-lap-times/', views.save_lap_times, name='save_lap_times'),
    path('sorted-lap-times/', views.display_sorted_lap_times, name='sorted_lap_times'),
    

    
    

]
