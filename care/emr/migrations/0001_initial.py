# Generated by Django 5.1.1 on 2024-11-13 16:51

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('facility', '0466_camera_presets'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllergyIntolerance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('clinical_status', models.CharField(blank=True, max_length=100, null=True)),
                ('verification_status', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('criticality', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.JSONField(default={})),
                ('onset', models.JSONField(default={})),
                ('recorded_date', models.DateTimeField(blank=True, null=True)),
                ('last_occurrence', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientconsultation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]