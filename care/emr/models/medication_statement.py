from django.db import models

from care.emr.models.base import EMRBaseModel


class MedicationStatement(EMRBaseModel):
    status = models.CharField(max_length=100)
    reason = models.CharField(max_length=100, null=True, blank=True)
    medication = models.JSONField(default=dict)
    patient = models.ForeignKey(
        "facility.PatientRegistration", on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        "facility.PatientConsultation", on_delete=models.CASCADE
    )
    effective_period = models.JSONField(default=dict)
    information_source = models.JSONField(default=dict)
    dosage = models.TextField(null=True, blank=True)
    note = models.TextField(null=True, blank=True)