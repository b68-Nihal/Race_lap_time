from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
import re

class Racer(models.Model):
    CATEGORY_CHOICES = [
        ('National', 'National'),
        ('Novice', 'Novice'),
    ]
    name = models.CharField(max_length=100)
    rider_number = models.CharField(max_length=10, unique=True)
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.rider_number}) - {self.category}"

class Group(models.Model):
    name = models.CharField(max_length=10)
    category = models.CharField(max_length=8, choices=Racer.CATEGORY_CHOICES)
    racers = models.ManyToManyField(Racer, related_name='groups')

    def __str__(self):
        return f"{self.name} - {self.category}"
    # class meta:
    #     unique_together = ('name', 'category','racers')



class LapTime(models.Model):
    racer = models.ForeignKey('Racer', on_delete=models.CASCADE, related_name='lap_times')
    lap_time = models.CharField(max_length=10)  # MM:SS.SSS format
    lap_number = models.IntegerField()

    def clean(self):
        # Validate the lap_time format
        if not re.match(r'^\d{2}:\d{2}\.\d{3}$', self.lap_time):
            raise ValidationError({'lap_time': "Lap time must be in MM:SS.SSS format."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('racer', 'lap_number')  # Assuming each lap number is unique per racer

    def __str__(self):
        return f"{self.racer.name} Lap {self.lap_number}: {self.lap_time}"

    
class SortedLapTime(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE, related_name='sorted_laptimes')
    lap_time = models.CharField(max_length=10)  # Keep the format MM:SS.SSS
    rank = models.IntegerField(help_text="Rank of the lap time from fastest to slowest")
    
    def __str__(self):
        return f"{self.racer.name} - {self.lap_time} (Rank: {self.rank})"
    
    class Meta:
        unique_together = ('racer', 'rank')
        ordering = ['racer', 'rank']


class RaceModeData(models.Model):
    racer = models.ForeignKey('Racer', on_delete=models.CASCADE, related_name='race_mode_data')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='race_mode_data')
    finish_position = models.CharField(max_length=10, blank=True, null=True)  # e.g., P1, P2, P3, DNF
    penalty = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} - {self.racer.name} - {self.finish_position}"
