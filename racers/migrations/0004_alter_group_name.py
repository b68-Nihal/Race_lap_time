# Generated by Django 5.0.2 on 2024-02-20 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racers', '0003_alter_racemodedata_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
