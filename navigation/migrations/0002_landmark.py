# Generated by Django 4.2.6 on 2023-10-11 17:48

import django.contrib.gis.db.models.fields
from django.db import migrations, models
from django.contrib.gis.geos import Point

def add_initial_data(apps, schema_editor):
    LandMarks = apps.get_model('navigation', 'LandMark')  # Replace 'your_app' with your app name
    LandMarks.objects.create(
        name='Donkey Travel',
        location=Point(float('5.048809728652404'), float('51.6514359606463'), srid=4326)
    )
class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandMark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.RunPython(add_initial_data),
    ]
