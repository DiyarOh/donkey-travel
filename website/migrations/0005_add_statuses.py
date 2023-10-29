from django.db import migrations

def add_statuses(apps, schema_editor):
    Status = apps.get_model('website', 'Status')

    # Create the four new statuses
    Status.objects.create(status_code=0, status='request', deletable=True, assign_pin=False)
    Status.objects.create(status_code=10, status='invoice', deletable=True, assign_pin=False)
    Status.objects.create(status_code=20, status='definite', deletable=False, assign_pin=True)
    Status.objects.create(status_code=30, status='archived', deletable=False, assign_pin=False)

def reverse_statuses(apps, schema_editor):
    Status = apps.get_model('website', 'Status')
    Status.objects.filter(status_code__in=[0, 10, 20, 30]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_booking_status'),
    ]

    operations = [
        migrations.RunPython(add_statuses, reverse_statuses),
    ]
