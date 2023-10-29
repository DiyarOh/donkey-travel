# Generated by Django 4.2.6 on 2023-10-29 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('navigation', '0007_alter_tracker_booking'),
        ('website', '0006_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='tracker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='navigation.tracker'),
        ),
    ]
