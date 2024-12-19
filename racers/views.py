# import json
# from django.forms import modelformset_factory
# from django.http import JsonResponse
# from django.shortcuts import redirect, render, get_object_or_404
# from .models import Group, RaceModeData, Racer, LapTime
# from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt
# from .forms import LapTimeForm, RaceModeDataForm, RaceModeDataFormSet, RacerRegistrationForm 
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
# from .models import Racer, LapTime
# import json
# from .models import Racer, LapTime
# from django.db.models import Min
# from django.shortcuts import render
# from .models import Group, Racer, LapTime
# from django.db.models import Min, F
# from collections import defaultdict
# from django.db import transaction
# from .models import Racer, LapTime, SortedLapTime
# from django.shortcuts import render
# from .models import SortedLapTime, Group
# from django.shortcuts import render, redirect
# from django.views.decorators.http import require_POST
# from .models import Racer, Group, RaceModeData
# from django.forms import modelformset_factory
# from django.shortcuts import render, redirect
# from .models import Group, Racer, SortedLapTime, RaceModeData
# from django.forms import modelformset_factory
# from .forms import RaceModeDataForm
# # This mapping could be defined outside the view function, perhaps in a utilities module or directly in the views.py


# def display_sorted_lap_times(request):
#     # Organize racers by category, then by group
#     categories = Group.objects.values_list('category', flat=True).distinct()
#     data_by_category = {}
    
#     for category in categories:
#         groups_in_category = Group.objects.filter(category=category)
#         data_by_group = {}
        
#         for group in groups_in_category:
#             racers_data = SortedLapTime.objects.filter(racer__groups=group).distinct('racer').prefetch_related('racer')
#             sorted_data = []
#             for racer_data in racers_data:
#                 racer_sorted_laps = SortedLapTime.objects.filter(racer=racer_data.racer).order_by('rank')[:3]
#                 sorted_data.append((racer_data.racer, racer_sorted_laps))
#             data_by_group[group.name] = sorted_data
        
#         data_by_category[category] = data_by_group

#     return render(request, 'racers/display_sorted_lap_times.html', {'data_by_category': data_by_category})


# def parse_lap_time(lap_time_str):
#     """Parse a lap time string formatted as MM:SS.SSS into total milliseconds."""
#     minutes, seconds = map(float, lap_time_str.split(':'))
#     return int(minutes) * 60000 + int(seconds * 1000)

# @transaction.atomic
# def process_and_sort_lap_times(racer_id):
    
    
#     """Process and sort lap times for a racer, then save them in SortedLapTime."""
#     try:
#         racer = Racer.objects.get(id=racer_id)
#         lap_times = LapTime.objects.filter(racer=racer).values_list('lap_time', flat=True)
#         # Parse lap times and sort them
#         parsed_times = sorted([parse_lap_time(time) for time in lap_times])
#         # Save sorted times
#         SortedLapTime.objects.filter(racer=racer).delete()  # Clear existing entries
#         for rank, time in enumerate(parsed_times, start=1):
#             # Convert back to MM:SS.SSS format for storage
#             minutes, ms = divmod(time, 60000)
#             seconds, ms = divmod(ms, 1000)
#             formatted_time = f"{minutes:02d}:{seconds:02d}.{ms:03d}"
#             SortedLapTime.objects.create(racer=racer, lap_time=formatted_time, rank=rank)
        

#     except Racer.DoesNotExist:
#         print("Racer not found")


# @csrf_exempt  # Consider CSRF protection for production
# @require_http_methods(["GET", "POST"])  # Restrict to GET and POST requests
# def qualifying_mode(request):
    
#         categories = Group.objects.values_list('category', flat=True).distinct()
#         groups_by_category = {category: Group.objects.filter(category=category) for category in categories}
#         return render(request, 'racers/qualifying_mode.html', {'groups_by_category': groups_by_category})

# @csrf_exempt  # Consider using proper CSRF protection for production
# @require_POST
# def save_lap_times(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         racerId = data.get('racerId')
#         lapNumber = data.get('lapNumber')
#         lapTime = data.get('lapTime')

#         # Ensure racer exists
#         try:
#             racer = Racer.objects.get(id=racerId)
#         except Racer.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Racer not found'}, status=404)

#         # Create or update the LapTime instance
#         LapTime.objects.update_or_create(
#             racer=racer,
#             lap_number=lapNumber,
#             defaults={'lap_time': lapTime}
#         )
#         process_and_sort_lap_times(racer.id)


#         return JsonResponse({'status': 'success', 'message': 'Lap time saved and sorted successfully'})
        

#     else:
#         return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        



# def homepage(request):
#     return render(request, 'racers/homepage.html')


# def register_racer(request):
#     if request.method == 'POST':
#         form = RacerRegistrationForm(request.POST)
#         if form.is_valid():
#             racer = form.save(commit=False)
#             group = form.cleaned_data['group']
#             if group:
#                 racer.save()
#                 racer.groups.add(group)
#                 racer.save()
#             else:
#                 racer.save()
#             return redirect('homepage')
#     else:
#         form = RacerRegistrationForm()
#     return render(request, 'racers/register_racer.html', {'form': form})



# def race_mode(request):
#     if request.method == 'POST':
#         FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
#         formset = FormSet(request.POST)
#         group = Group.objects.all()
#         racers =  Racer.objects.all()
#         for group in group:
#             category = group.category
#             group_name = group.name
#             group_id = group.id
#             for racer in racers:
#                 query_for_finish_position = 'form-'+category+'-'+group_name+'-'+str(racer.id)+'-finish_position'
#                 query_for_penalty = 'form-'+category+'-'+group_name+'-'+str(racer.id)+'-penalty'
#                 finish_position = request.POST.get(query_for_finish_position)
#                 penalty = request.POST.get(query_for_penalty)

#                 if finish_position :
#                     # print(f'Finish Position: {finish_position}')
#                     # print(f'Penalty: {penalty}')
#                     racer = Racer.objects.get(id=racer.id)
#                     group = Group.objects.get(id=group_id)
#                     RaceModeData.objects.create(
#                         racer=racer, 
#                         group=group, 
#                         finish_position=finish_position, 
#                         penalty=penalty)
#         return redirect('race_mode')  # Redirect or update as neededS
#     else:
#         FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
#         formset = FormSet(queryset=RaceModeData.objects.none())  # Adjust as needed
        
#     categories_groups = Group.objects.prefetch_related('racers__sorted_laptimes').all()
#     race_data = {}
#     for group in categories_groups:
#         for racer in group.racers.all():
#             sorted_laps = racer.sorted_laptimes.order_by('rank')[:3]
#             if group.category not in race_data:
#                 race_data[group.category] = {}
#             if group.name not in race_data[group.category]:
#                 race_data[group.category][group.name] = []
#             race_data[group.category][group.name].append({
#                 'racer': racer,
#                 'sorted_laps': sorted_laps
#             })

#     # Sort each group's racers based on lap times
#     for category, groups in race_data.items():
#         for group_name, racers in groups.items():
#             racers.sort(key=lambda x: (
#                 parse_lap_time(x['sorted_laps'][0].lap_time if len(x['sorted_laps']) > 0 else "99:59.999"),
#                 parse_lap_time(x['sorted_laps'][1].lap_time if len(x['sorted_laps']) > 1 else "99:59.999"),
#                 parse_lap_time(x['sorted_laps'][2].lap_time if len(x['sorted_laps']) > 2 else "99:59.999"),
#             ))
    
#     return render(request, 'racers/race_mode.html', {'race_data': race_data, 'formset': formset})
    
# @transaction.atomic
# def generate_new_groups(request):
#     # Define mappings for novice category advancement
#     novice_mappings = {
#         'A': 'G', 'B': 'G',
#         'C': 'H', 'D': 'H',
#         'E': 'I', 'F': 'I',
#         # 'G': 'L', 'H': 'L',
#         # 'I': 'M', 'J': 'M',
#         # 'K': 'N', 'L': 'N',
#         'G': 'J', 'H': 'J', 'I':"J",
#     }
    
#     # Define mappings for national category advancement
#     national_mappings = {
#         'A': 'National_Finals', 'B': 'National_Finals',
#         #'C': 'E', 'D': 'National_Finals', 'E': 'National_Finals',
#     }

#     def create_or_update_group(group_name, category, racer):
#         group, created = Group.objects.get_or_create(name=group_name, category=category)
#         racer.groups.add(group)

#     def process_novice_category():
#         for data in RaceModeData.objects.filter(group__category='Novice').select_related('racer', 'group'):
#             if data.finish_position in ['P1', 'P2', 'P3','P4']:
#                 new_group_name = novice_mappings.get(data.group.name)
#                 if new_group_name:
#                     create_or_update_group(new_group_name, 'Novice', data.racer)

#     # def process_national_category():
#     #     for data in RaceModeData.objects.filter(group__category='National').select_related('racer', 'group'):
#     #         if data.group.name == 'B':
#     #             if data.finish_position in ['P1', 'P3']:
#     #                 create_or_update_group('D', 'National', data.racer)
#     #             elif data.finish_position in ['P2', 'P4']:
#     #                 create_or_update_group('E', 'National', data.racer)
#     #         elif data.group.name in ['D', 'E']:
#     #             if data.finish_position in ['P1', 'P2', 'P3']:
#     #                 create_or_update_group('National_Finals', 'National', data.racer)
#     #         else:
#     #             new_group_name = national_mappings.get(data.group.name)
#     #             if isinstance(new_group_name, list):
#     #                 # Assuming only 'B' maps to multiple groups, handled above
#     #                 pass
#     #             elif new_group_name and data.finish_position in ['P1', 'P2', 'P3', 'P4']:
#     #                 create_or_update_group(new_group_name, 'National', data.racer)
#     def process_national_category():
#          for data in RaceModeData.objects.filter(group__category='National').select_related('racer', 'group'):
#             if data.finish_position in ['P1', 'P2', 'P3']:
#                 new_group_name = national_mappings.get(data.group.name)
#                 if new_group_name:
#                     create_or_update_group(new_group_name, 'National', data.racer)

#     # Process both categories
#     process_novice_category()
#     process_national_category()

#     return redirect('homepage')
import json
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.db.models import Min, F
from collections import defaultdict

from .models import Group, RaceModeData, Racer, LapTime, SortedLapTime
from .forms import LapTimeForm, RaceModeDataForm, RaceModeDataFormSet, RacerRegistrationForm
from django.template.defaulttags import register

def homepage(request):
    """Render the homepage."""
    return render(request, 'racers/homepage.html')

def display_sorted_lap_times(request):
    """Display sorted lap times organized by category and group."""
    categories = Group.objects.values_list('category', flat=True).distinct()
    data_by_category = {}
    
    for category in categories:
        groups_in_category = Group.objects.filter(category=category)
        data_by_group = {}
        
        for group in groups_in_category:
            racers_data = SortedLapTime.objects.filter(
                racer__groups=group
            ).distinct('racer').prefetch_related('racer')
            
            sorted_data = []
            for racer_data in racers_data:
                racer_sorted_laps = SortedLapTime.objects.filter(
                    racer=racer_data.racer
                ).order_by('rank')[:3]
                sorted_data.append((racer_data.racer, racer_sorted_laps))
            
            data_by_group[group.name] = sorted_data
        data_by_category[category] = data_by_group

    return render(request, 'racers/display_sorted_lap_times.html', 
                 {'data_by_category': data_by_category})

def parse_lap_time(lap_time_str):
    """Parse a lap time string formatted as MM:SS.SSS into total milliseconds."""
    try:
        minutes, seconds = map(float, lap_time_str.split(':'))
        return int(minutes) * 60000 + int(seconds * 1000)
    except ValueError:
        return float('inf')  # Return infinity for invalid times

@transaction.atomic
def process_and_sort_lap_times(racer_id):
    """Process and sort lap times for a racer, storing them in SortedLapTime."""
    try:
        racer = Racer.objects.get(id=racer_id)
        lap_times = LapTime.objects.filter(racer=racer).values_list('lap_time', flat=True)
        
        # Parse and sort lap times
        parsed_times = sorted([parse_lap_time(time) for time in lap_times])
        
        # Clear existing entries and save new sorted times
        SortedLapTime.objects.filter(racer=racer).delete()
        
        for rank, time in enumerate(parsed_times, start=1):
            minutes, ms = divmod(time, 60000)
            seconds, ms = divmod(ms, 1000)
            formatted_time = f"{minutes:02d}:{seconds:02d}.{ms:03d}"
            
            SortedLapTime.objects.create(
                racer=racer,
                lap_time=formatted_time,
                rank=rank
            )
    except Racer.DoesNotExist:
        print(f"Racer with ID {racer_id} not found")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def qualifying_mode(request):
    """Handle qualifying mode view."""
    categories = Group.objects.values_list('category', flat=True).distinct()
    groups_by_category = {
        category: Group.objects.filter(category=category) 
        for category in categories
    }
    return render(request, 'racers/qualifying_mode.html', 
                 {'groups_by_category': groups_by_category})

@csrf_exempt
@require_POST
def save_lap_times(request):
    """Save lap times for a racer."""
    try:
        data = json.loads(request.body)
        racer_id = data.get('racerId')
        lap_number = data.get('lapNumber')
        lap_time = data.get('lapTime')

        racer = Racer.objects.get(id=racer_id)
        
        # Create or update lap time
        LapTime.objects.update_or_create(
            racer=racer,
            lap_number=lap_number,
            defaults={'lap_time': lap_time}
        )
        
        # Process and sort the updated lap times
        process_and_sort_lap_times(racer.id)

        return JsonResponse({
            'status': 'success',
            'message': 'Lap time saved and sorted successfully'
        })

    except Racer.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Racer not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def register_racer(request):
    """Handle racer registration."""
    if request.method == 'POST':
        form = RacerRegistrationForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            group = form.cleaned_data['group']
            
            racer.save()
            if group:
                racer.groups.add(group)
            
            return redirect('homepage')
    else:
        form = RacerRegistrationForm()
    
    return render(request, 'racers/register_racer.html', {'form': form})

def race_mode(request):
    """Handle race mode view and form submission."""
    if request.method == 'POST':
        FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
        formset = FormSet(request.POST)
        
        # Process form data for each group and racer
        for group in Group.objects.all():
            category = group.category
            group_name = group.name
            
            for racer in Racer.objects.all():
                finish_position = request.POST.get(
                    f'form-{category}-{group_name}-{racer.id}-finish_position'
                )
                penalty = request.POST.get(
                    f'form-{category}-{group_name}-{racer.id}-penalty'
                )

                # Only create record if finish_position is not N/A
                if finish_position and finish_position != 'N/A':
                    RaceModeData.objects.create(
                        racer=racer,
                        group=group,
                        finish_position=finish_position,
                        penalty=penalty if penalty else None
                    )
        
        return redirect('race_mode')
    
    else:
        FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
        formset = FormSet(queryset=RaceModeData.objects.none())
    
    # Prepare race data for template
    categories_groups = Group.objects.prefetch_related('racers__sorted_laptimes').all()
    race_data = {}
    
    for group in categories_groups:
        for racer in group.racers.all():
            sorted_laps = racer.sorted_laptimes.order_by('rank')[:3]
            
            if group.category not in race_data:
                race_data[group.category] = {}
            if group.name not in race_data[group.category]:
                race_data[group.category][group.name] = []
                
            race_data[group.category][group.name].append({
                'racer': racer,
                'sorted_laps': sorted_laps
            })

    # Sort racers in each group based on lap times
    for category, groups in race_data.items():
        for group_name, racers in groups.items():
            racers.sort(key=lambda x: (
                parse_lap_time(x['sorted_laps'][0].lap_time if len(x['sorted_laps']) > 0 else "99:59.999"),
                parse_lap_time(x['sorted_laps'][1].lap_time if len(x['sorted_laps']) > 1 else "99:59.999"),
                parse_lap_time(x['sorted_laps'][2].lap_time if len(x['sorted_laps']) > 2 else "99:59.999")
            ))
    
    return render(request, 'racers/race_mode.html', 
                 {'race_data': race_data, 'formset': formset})

@transaction.atomic
def generate_new_groups(request):
    """Generate new groups based on race results."""
    # Novice category advancement mappings
    novice_round1_mappings = {
        'A': 'Quarter_1', 'B': 'Quarter_1',  # Top 3 from A and B go to Quarter_1
        'C': 'Quarter_2', 'D': 'Quarter_2',  # Top 3 from C and D go to Quarter_2
        'E': 'Quarter_3', 'F': 'Quarter_3'   # Top 3 from E and F go to Quarter_3
    }
    
    novice_round2_mappings = {
        'Quarter_1': 'Semi_1',  # Top 4 go to Semi_1
        'Quarter_2': 'Semi_2',  # Top 4 go to Semi_2
        'Quarter_3': 'Semi_1'   # Top 4 split between Semi_1 and Semi_2
    }
    
    novice_round3_mappings = {
        'Semi_1': 'Final',  # Top 3 go to Final
        'Semi_2': 'Final'   # Top 3 go to Final
    }
    
    national_mappings = {
        'N1': 'Final',  # Top 3 go to Final
        'N2': 'Final'   # Top 3 go to Final
    }

    def create_or_update_group(group_name, category, racer):
        """Create or update group and add racer to it."""
        group, created = Group.objects.get_or_create(name=group_name, category=category)
        racer.groups.add(group)

    def process_novice_round1():
        """Process Heat round (Round 1)."""
        for data in RaceModeData.objects.filter(
            group__category='Novice',
            group__name__in=['A', 'B', 'C', 'D', 'E', 'F']
        ).select_related('racer', 'group'):
            if data.finish_position in ['P1', 'P2', 'P3']:
                new_group_name = novice_round1_mappings.get(data.group.name)
                if new_group_name:
                    create_or_update_group(new_group_name, 'Novice', data.racer)

    def process_novice_round2():
        """Process Quarter Finals (Round 2)."""
        for data in RaceModeData.objects.filter(
            group__category='Novice',
            group__name__in=['Quarter_1', 'Quarter_2', 'Quarter_3']
        ).select_related('racer', 'group'):
            if data.finish_position in ['P1', 'P2', 'P3', 'P4']:
                new_group_name = novice_round2_mappings.get(data.group.name)
                if new_group_name:
                    if data.group.name == 'Quarter_3':
                        position = int(data.finish_position[1])
                        new_group_name = 'Semi_1' if position in [1, 3] else 'Semi_2'
                    create_or_update_group(new_group_name, 'Novice', data.racer)

    def process_novice_round3():
        """Process Semi Finals (Round 3)."""
        for data in RaceModeData.objects.filter(
            group__category='Novice',
            group__name__in=['Semi_1', 'Semi_2']
        ).select_related('racer', 'group'):
            if data.finish_position in ['P1', 'P2', 'P3']:
                new_group_name = novice_round3_mappings.get(data.group.name)
                if new_group_name:
                    create_or_update_group(new_group_name, 'Novice', data.racer)

    def process_national_category():
        """Process National category advancement."""
        for data in RaceModeData.objects.filter(
            group__category='National'
        ).select_related('racer', 'group'):
            if data.finish_position in ['P1', 'P2', 'P3']:
                new_group_name = national_mappings.get(data.group.name)
                if new_group_name:
                    create_or_update_group(new_group_name, 'National', data.racer)

    # Process all rounds
    process_novice_round1()
    process_novice_round2()
    process_novice_round3()
    process_national_category()

    return redirect('homepage')

def display_results(request):
    """Display race results organized by category and group."""
    categories = Group.objects.values_list('category', flat=True).distinct()
    results_by_category = {}
    
    for category in categories:
        groups_in_category = Group.objects.filter(category=category)
        results_by_group = {}
        
        for group in groups_in_category:
            # Get all race results for this group
            race_results = RaceModeData.objects.filter(
                group=group
            ).select_related('racer').order_by('finish_position')
            
            results_by_group[group.name] = race_results
            
        results_by_category[category] = results_by_group

    return render(request, 'racers/display_results.html', 
                 {'results_by_category': results_by_category})
    
def display_racers(request):
    """Display all racers with basic information."""
    # Get all racers ordered by name
    racers = Racer.objects.all().order_by('name')

    context = {
        'racers': racers,
    }

    return render(request, 'racers/display_racers.html', context)
# Add to views.py

def display_qualifying_results(request):
    """Display qualifying results organized by category and group."""
    # Get all categories
    categories = Group.objects.values_list('category', flat=True).distinct()
    results_by_category = {}
    
    for category in categories:
        groups_in_category = Group.objects.filter(category=category)
        results_by_group = {}
        
        for group in groups_in_category:
            # Get all racers in this group with their best lap times
            racers_with_times = []
            for racer in group.racers.all():
                best_lap = LapTime.objects.filter(racer=racer).order_by('lap_time').first()
                if best_lap:
                    racers_with_times.append({
                        'position': None,  # Will be set after sorting
                        'name': racer.name,
                        'number': racer.rider_number,
                        'best_lap_time': best_lap.lap_time
                    })
            
            # Sort racers by best lap time
            racers_with_times.sort(key=lambda x: x['best_lap_time'])
            
            # Assign positions
            for i, racer in enumerate(racers_with_times, 1):
                racer['position'] = i
            
            results_by_group[group.name] = racers_with_times
            
        results_by_category[category] = results_by_group

    return render(request, 'racers/qualifying_results.html', 
                 {'results_by_category': results_by_category})

def display_attendance_sheet(request):
    """Display attendance sheet organized by category and group."""
    categories = Group.objects.values_list('category', flat=True).distinct()
    attendance_data = {}
    
    for category in categories:
        groups_in_category = Group.objects.filter(category=category)
        group_data = {}
        
        for group in groups_in_category:
            racers = group.racers.all().order_by('rider_number')
            group_data[group.name] = racers
            
        attendance_data[category] = group_data

    return render(request, 'racers/attendance_sheet.html', 
                 {'attendance_data': attendance_data})
def individual_laptime_sheets(request, group_id=None):
    """Generate individual lap time recording sheets for each timekeeper."""
    if not group_id:
        groups = Group.objects.all()
        return render(request, 'racers/select_group.html', {'groups': groups})
    
    group = get_object_or_404(Group, id=group_id)
    racers = group.racers.all()
    
    context = {
        'group': group,
        'racers': racers,
    }
    return render(request, 'racers/individual_laptime_sheets.html', context)
# Add to views.py

from django.shortcuts import render
from .models import Group

# def timekeeper_sheets(request):
#     """Generate sheets organized by timekeeper."""
#     # Get all groups ordered by category and name
#     groups = Group.objects.all().order_by('category', 'name')
    
#     # Prepare data for 6 timekeepers
#     timekeeper_data = []
    
#     for i in range(6):  # For 6 timekeepers
#         assignments = []
#         for group in groups:
#             riders = list(group.racers.all())
#             if i < len(riders):  # If there's a rider at this index
#                 assignments.append({
#                     'rider': riders[i],
#                     'group': group
#                 })
        
#         # Create pairs of assignments (for 2 per page)
#         paired_assignments = []
#         for j in range(0, len(assignments), 2):
#             pair = assignments[j:j+2]
#             paired_assignments.append(pair)
            
#         timekeeper_data.append({
#             'number': i + 1,
#             'paired_assignments': paired_assignments
#         })

#     return render(request, 'racers/timekeeper_sheets.html', 
#                  {'timekeeper_data': timekeeper_data})

def timekeeper_sheets(request):
    """Generate sheets organized by timekeeper."""
    groups = Group.objects.all().order_by('category', 'name')
    
    timekeeper_data = []
    for i in range(6):  # For 6 timekeepers
        assignments = []
        for group in groups:
            riders = list(group.racers.all())
            if i < len(riders):
                assignments.append({
                    'rider': riders[i],
                    'group': group
                })
        
        # Create pairs of assignments
        paired_assignments = []
        for j in range(0, len(assignments), 2):
            pair = assignments[j:j+2]
            paired_assignments.append(pair)
            
        timekeeper_data.append({
            'number': i + 1,
            'paired_assignments': paired_assignments
        })

    return render(request, 'racers/timekeeper_sheets.html', 
                 {'timekeeper_data': timekeeper_data})
    

@register.filter
def grouper(items, n):
    """Group items into pairs."""
    args = [iter(items)] * n
    return zip(*args)

@register.filter
def divide_by(value, arg):
    try:
        return int(value) / int(arg)
    except (ValueError, ZeroDivisionError):
        return None

@register.filter
def ceil(value):
    import math
    try:
        return math.ceil(value)
    except (ValueError, TypeError):
        return None