from django.db import models
from django.core.exceptions import ValidationError
import re

class Racer(models.Model):
    CATEGORY_CHOICES = [
        ('National', 'National'),
        ('Novice', 'Novice'),
        ('Nari', 'Nari'),
    ]

    name = models.CharField(max_length=100)
    rider_number = models.CharField(max_length=10)
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    transponder_id = models.CharField(max_length=20, blank=True, null=True, help_text="Assigned transponder ID during qualifying")

    def __str__(self):
        return f"{self.name} ({self.rider_number}) - {self.category}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['rider_number', 'category'], name='unique_rider_per_category')
        ]

class Group(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=8, choices=Racer.CATEGORY_CHOICES)
    racers = models.ManyToManyField(Racer, related_name='groups')

    def __str__(self):
        return f"{self.name} - {self.category}"

    class Meta:
        unique_together = ('name', 'category')


class LapTime(models.Model):
    racer = models.ForeignKey('Racer', on_delete=models.CASCADE, related_name='lap_times')
    lap_time = models.CharField(max_length=10)  # Format MM:SS.SSS
    lap_number = models.IntegerField()

    def clean(self):
        if not re.match(r'^\d{2}:\d{2}\.\d{3}$', self.lap_time):
            raise ValidationError({'lap_time': "Lap time must be in MM:SS.SSS format."})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('racer', 'lap_number')

    def __str__(self):
        return f"{self.racer.name} Lap {self.lap_number}: {self.lap_time}"


class SortedLapTime(models.Model):
    racer = models.ForeignKey(Racer, on_delete=models.CASCADE, related_name='sorted_laptimes')
    lap_time = models.CharField(max_length=10)
    rank = models.IntegerField(help_text="Rank of the lap time from fastest to slowest")

    def __str__(self):
        return f"{self.racer.name} - {self.lap_time} (Rank: {self.rank})"

    class Meta:
        unique_together = ('racer', 'rank')
        ordering = ['racer', 'rank']


class RaceModeData(models.Model):
    racer = models.ForeignKey('Racer', on_delete=models.CASCADE, related_name='race_mode_data')
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='race_mode_data')
    finish_position = models.CharField(max_length=10, blank=True, null=True)  # e.g., P1, P2, DNF
    penalty = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} - {self.racer.name} - {self.finish_position}"

    class Meta:
        unique_together = ('racer', 'group')
        
class Transponder(models.Model):
    transponder_id = models.CharField(max_length=20, unique=True)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return self.transponder_id

class Heat(models.Model):
    category = models.CharField(max_length=50)
    group = models.CharField(max_length=10)
    heat_number = models.IntegerField()

    def __str__(self):
        return f"{self.category} - Group {self.group} - Heat {self.heat_number}"

class HeatAssignment(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    racer = models.ForeignKey('Racer', on_delete=models.CASCADE)
    transponder = models.ForeignKey(Transponder, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.heat}: {self.racer.name} ({self.transponder})"
