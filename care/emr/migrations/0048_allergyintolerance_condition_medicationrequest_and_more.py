# Generated by Django 5.1.3 on 2024-12-27 17:53

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0047_remove_condition_created_by_and_more'),
        ('facility', '0479_patientconsultationicmr_patienticmr_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('meta', models.JSONField(default=dict)),
                ('clinical_status', models.CharField(blank=True, max_length=100, null=True)),
                ('verification_status', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('criticality', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.JSONField(default=dict)),
                ('onset', models.JSONField(default=dict)),
                ('recorded_date', models.DateTimeField(blank=True, null=True)),
                ('last_occurrence', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('meta', models.JSONField(default=dict)),
                ('clinical_status', models.CharField(blank=True, max_length=100, null=True)),
                ('verification_status', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('severity', models.CharField(blank=True, max_length=100, null=True)),
                ('code', models.JSONField(default=dict)),
                ('body_site', models.JSONField(default=dict)),
                ('onset', models.JSONField(default=dict)),
                ('recorded_date', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MedicationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('meta', models.JSONField(default=dict)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('status_reason', models.CharField(blank=True, max_length=100, null=True)),
                ('status_changed', models.DateTimeField(blank=True, null=True)),
                ('intent', models.CharField(blank=True, max_length=100, null=True)),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('priority', models.CharField(blank=True, max_length=100, null=True)),
                ('do_not_perform', models.BooleanField()),
                ('method', models.JSONField(blank=True, default=dict, null=True)),
                ('authored_on', models.DateTimeField(blank=True, null=True)),
                ('dosage_instruction', models.JSONField(blank=True, default=list, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
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
                ('information_source', models.CharField(max_length=100)),
                ('dosage_text', models.TextField(blank=True, null=True)),
                ('note', models.TextField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QuestionnaireResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('meta', models.JSONField(default=dict)),
                ('subject_id', models.UUIDField()),
                ('responses', models.JSONField(default=list)),
                ('structured_responses', models.JSONField(default=dict)),
                ('structured_response_type', models.CharField(blank=True, default=None, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('questionnaire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emr.questionnaire')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.UUIDField(db_index=True, default=uuid.uuid4, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('history', models.JSONField(default=dict)),
                ('meta', models.JSONField(default=dict)),
                ('status', models.CharField(max_length=255)),
                ('is_group', models.BooleanField(default=False)),
                ('category', models.JSONField(default=dict)),
                ('main_code', models.JSONField(default=dict)),
                ('alternate_coding', models.JSONField(default=list)),
                ('subject_type', models.CharField(max_length=255)),
                ('subject_id', models.UUIDField()),
                ('effective_datetime', models.DateTimeField()),
                ('performer', models.JSONField(default=dict)),
                ('value_type', models.CharField(max_length=255)),
                ('value', models.JSONField()),
                ('note', models.TextField()),
                ('body_site', models.JSONField(default=dict)),
                ('method', models.JSONField(default=dict)),
                ('reference_range', models.JSONField(default=list)),
                ('interpretation', models.CharField(max_length=255)),
                ('parent', models.UUIDField(null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_created_by', to=settings.AUTH_USER_MODEL)),
                ('data_entered_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations_entered', to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.encounter')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facility.patientregistration')),
                ('updated_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(app_label)s_%(class)s_updated_by', to=settings.AUTH_USER_MODEL)),
                ('questionnaire_response', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='emr.questionnaireresponse')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]