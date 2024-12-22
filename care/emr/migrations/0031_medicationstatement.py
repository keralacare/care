# Generated by Django 5.1.3 on 2024-12-22 03:28

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0030_alter_questionnaireresponse_encounter'),
        ('facility', '0470_alter_historicalpatientregistration_is_antenatal_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationStatement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('meta', models.JSONField(default=dict)),
                ('status', models.CharField(max_length=100)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('medication', models.JSONField(default=dict)),
                ('effective_period', models.JSONField(default=dict)),
                ('information_source', models.JSONField(default=dict)),
                ('dosage', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientconsultation')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
