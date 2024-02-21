import json
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Group, RaceModeData, Racer, LapTime
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import LapTimeForm, RaceModeDataForm, RaceModeDataFormSet, RacerRegistrationForm 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Racer, LapTime
import json
from .models import Racer, LapTime
from django.db.models import Min
from django.shortcuts import render
from .models import Group, Racer, LapTime
from django.db.models import Min, F
from collections import defaultdict
from django.db import transaction
from .models import Racer, LapTime, SortedLapTime
from django.shortcuts import render
from .models import SortedLapTime, Group
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Racer, Group, RaceModeData
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from .models import Group, Racer, SortedLapTime, RaceModeData
from django.forms import modelformset_factory
from .forms import RaceModeDataForm
# This mapping could be defined outside the view function, perhaps in a utilities module or directly in the views.py


def display_sorted_lap_times(request):
    # Organize racers by category, then by group
    categories = Group.objects.values_list('category', flat=True).distinct()
    data_by_category = {}
    
    for category in categories:
        groups_in_category = Group.objects.filter(category=category)
        data_by_group = {}
        
        for group in groups_in_category:
            racers_data = SortedLapTime.objects.filter(racer__groups=group).distinct('racer').prefetch_related('racer')
            sorted_data = []
            for racer_data in racers_data:
                racer_sorted_laps = SortedLapTime.objects.filter(racer=racer_data.racer).order_by('rank')[:3]
                sorted_data.append((racer_data.racer, racer_sorted_laps))
            data_by_group[group.name] = sorted_data
        
        data_by_category[category] = data_by_group

    return render(request, 'racers/display_sorted_lap_times.html', {'data_by_category': data_by_category})


def parse_lap_time(lap_time_str):
    """Parse a lap time string formatted as MM:SS.SSS into total milliseconds."""
    minutes, seconds = map(float, lap_time_str.split(':'))
    return int(minutes) * 60000 + int(seconds * 1000)

@transaction.atomic
def process_and_sort_lap_times(racer_id):
    
    
    """Process and sort lap times for a racer, then save them in SortedLapTime."""
    try:
        racer = Racer.objects.get(id=racer_id)
        lap_times = LapTime.objects.filter(racer=racer).values_list('lap_time', flat=True)
        # Parse lap times and sort them
        parsed_times = sorted([parse_lap_time(time) for time in lap_times])
        # Save sorted times
        SortedLapTime.objects.filter(racer=racer).delete()  # Clear existing entries
        for rank, time in enumerate(parsed_times, start=1):
            # Convert back to MM:SS.SSS format for storage
            minutes, ms = divmod(time, 60000)
            seconds, ms = divmod(ms, 1000)
            formatted_time = f"{minutes:02d}:{seconds:02d}.{ms:03d}"
            SortedLapTime.objects.create(racer=racer, lap_time=formatted_time, rank=rank)
        

    except Racer.DoesNotExist:
        print("Racer not found")


@csrf_exempt  # Consider CSRF protection for production
@require_http_methods(["GET", "POST"])  # Restrict to GET and POST requests
def qualifying_mode(request):
    
        categories = Group.objects.values_list('category', flat=True).distinct()
        groups_by_category = {category: Group.objects.filter(category=category) for category in categories}
        return render(request, 'racers/qualifying_mode.html', {'groups_by_category': groups_by_category})

@csrf_exempt  # Consider using proper CSRF protection for production
@require_POST
def save_lap_times(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        racerId = data.get('racerId')
        lapNumber = data.get('lapNumber')
        lapTime = data.get('lapTime')

        # Ensure racer exists
        try:
            racer = Racer.objects.get(id=racerId)
        except Racer.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Racer not found'}, status=404)

        # Create or update the LapTime instance
        LapTime.objects.update_or_create(
            racer=racer,
            lap_number=lapNumber,
            defaults={'lap_time': lapTime}
        )
        process_and_sort_lap_times(racer.id)


        return JsonResponse({'status': 'success', 'message': 'Lap time saved and sorted successfully'})
        

    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
        



def homepage(request):
    return render(request, 'racers/homepage.html')


def register_racer(request):
    if request.method == 'POST':
        form = RacerRegistrationForm(request.POST)
        if form.is_valid():
            racer = form.save(commit=False)
            group = form.cleaned_data['group']
            if group:
                racer.save()
                racer.groups.add(group)
                racer.save()
            else:
                racer.save()
            return redirect('homepage')
    else:
        form = RacerRegistrationForm()
    return render(request, 'racers/register_racer.html', {'form': form})



def race_mode(request):
    if request.method == 'POST':
        FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
        formset = FormSet(request.POST)
        group = Group.objects.all()
        racers =  Racer.objects.all()
        for group in group:
            category = group.category
            group_name = group.name
            group_id = group.id
            for racer in racers:
                query_for_finish_position = 'form-'+category+'-'+group_name+'-'+str(racer.id)+'-finish_position'
                query_for_penalty = 'form-'+category+'-'+group_name+'-'+str(racer.id)+'-penalty'
                finish_position = request.POST.get(query_for_finish_position)
                penalty = request.POST.get(query_for_penalty)

                if finish_position :
                    # print(f'Finish Position: {finish_position}')
                    # print(f'Penalty: {penalty}')
                    racer = Racer.objects.get(id=racer.id)
                    group = Group.objects.get(id=group_id)
                    RaceModeData.objects.create(
                        racer=racer, 
                        group=group, 
                        finish_position=finish_position, 
                        penalty=penalty)
        return redirect('race_mode')  # Redirect or update as neededS
    else:
        FormSet = modelformset_factory(RaceModeData, form=RaceModeDataForm, extra=0)
        formset = FormSet(queryset=RaceModeData.objects.none())  # Adjust as needed
        
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

    # Sort each group's racers based on lap times
    for category, groups in race_data.items():
        for group_name, racers in groups.items():
            racers.sort(key=lambda x: (
                parse_lap_time(x['sorted_laps'][0].lap_time if len(x['sorted_laps']) > 0 else "99:59.999"),
                parse_lap_time(x['sorted_laps'][1].lap_time if len(x['sorted_laps']) > 1 else "99:59.999"),
                parse_lap_time(x['sorted_laps'][2].lap_time if len(x['sorted_laps']) > 2 else "99:59.999"),
            ))
    
    return render(request, 'racers/race_mode.html', {'race_data': race_data, 'formset': formset})
    
@transaction.atomic
def generate_new_groups(request):
    # Define mappings for novice category advancement
    novice_mappings = {
        'A': 'I', 'B': 'I',
        'C': 'J', 'D': 'J',
        'E': 'K', 'F': 'K',
        'G': 'L', 'H': 'L',
        'I': 'M', 'J': 'M',
        'K': 'N', 'L': 'N',
        'M': 'Novice_Finals', 'N': 'Novice_Finals',
    }
    
    # Define mappings for national category advancement
    national_mappings = {
        'A': 'D', 'B': ['D', 'E'], 'C': 'E', 'D': 'National_Finals', 'E': 'National_Finals',
    }

    def create_or_update_group(group_name, category, racer):
        group, created = Group.objects.get_or_create(name=group_name, category=category)
        racer.groups.add(group)

    def process_novice_category():
        for data in RaceModeData.objects.filter(group__category='Novice').select_related('racer', 'group'):
            if data.finish_position in ['P1', 'P2', 'P3']:
                new_group_name = novice_mappings.get(data.group.name)
                if new_group_name:
                    create_or_update_group(new_group_name, 'Novice', data.racer)

    def process_national_category():
        for data in RaceModeData.objects.filter(group__category='National').select_related('racer', 'group'):
            if data.group.name == 'B':
                if data.finish_position in ['P1', 'P3']:
                    create_or_update_group('D', 'National', data.racer)
                elif data.finish_position in ['P2', 'P4']:
                    create_or_update_group('E', 'National', data.racer)
            elif data.group.name in ['D', 'E']:
                if data.finish_position in ['P1', 'P2', 'P3']:
                    create_or_update_group('National_Finals', 'National', data.racer)
            else:
                new_group_name = national_mappings.get(data.group.name)
                if isinstance(new_group_name, list):
                    # Assuming only 'B' maps to multiple groups, handled above
                    pass
                elif new_group_name and data.finish_position in ['P1', 'P2', 'P3', 'P4']:
                    create_or_update_group(new_group_name, 'National', data.racer)

    # Process both categories
    process_novice_category()
    process_national_category()

    return redirect('homepage')