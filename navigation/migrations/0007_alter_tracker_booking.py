# Generated by Django 4.2.6 on 2023-10-29 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_customer_user'),
        ('navigation', '0006_alter_tracker_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracker',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trackers', to='website.booking'),
        ),
    ]