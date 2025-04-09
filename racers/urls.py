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
    path('generate-groups/', views.generate_new_groups, name='generate_new_groups'),
    path('results/', views.display_results, name='display_results'),
    path('racers/', views.display_racers, name='display_racers'),
    path('qualifying-results/', views.display_qualifying_results, name='qualifying_results'),
    path('attendance-sheet/', views.display_attendance_sheet, name='attendance_sheet'),
    path('individual-laptime/', views.individual_laptime_sheets, name='individual_laptime_sheets'),
    path('individual-laptime/<int:group_id>/', views.individual_laptime_sheets, name='individual_laptime_sheets'),
    path('timekeeper-sheets/', views.timekeeper_sheets, name='timekeeper_sheets'),
    path('qualifying-schedule/', views.qualifying_schedule_view, name='qualifying_schedule'),
    # path('qualifying-schedule/', views.qualifying_schedule, name='qualifying_schedule'),
    path("heat-assignments/", views.heat_assignment_list, name="heat_assignments"),


    
    

]
