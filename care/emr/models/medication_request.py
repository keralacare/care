from django.db import models

from care.emr.models.base import EMRBaseModel


class MedicationRequest(EMRBaseModel):
    status = models.CharField(max_length=100, null=True, blank=True)
    status_reason = models.CharField(max_length=100, null=True, blank=True)
    status_changed = models.DateTimeField(null=True, blank=True)
    intent = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    priority = models.CharField(max_length=100, null=True, blank=True)
    do_not_perform = models.BooleanField()
    method = models.JSONField(default=dict, null=True, blank=True)
    patient = models.ForeignKey(
        "facility.PatientRegistration", on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        "facility.PatientConsultation", on_delete=models.CASCADE
    )
    authored_on = models.DateTimeField(null=True, blank=True)
    dosage_instruction = models.JSONField(default=list, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
