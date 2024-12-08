from django.db import models

from care.emr.models.base import EMRBaseModel


class Condition(EMRBaseModel):
    clinical_status = models.CharField(max_length=100, null=True, blank=True)
    verification_status = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    severity = models.CharField(max_length=100, null=True, blank=True)
    code = models.JSONField(default=dict, null=False, blank=False)
    body_site = models.JSONField(default=dict, null=False, blank=False)
    patient = models.ForeignKey(
        "facility.PatientRegistration", on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        "facility.PatientConsultation", on_delete=models.CASCADE
    )
    onset = models.JSONField(default=dict)
    recorded_date = models.DateTimeField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)
