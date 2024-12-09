from django.db import models

from care.emr.models.base import EMRBaseModel
from care.emr.models.service_request import ServiceRequest
from care.facility.models.patient import PatientRegistration
from care.users.models import User


class Specimen(EMRBaseModel):
    identifier = models.CharField(max_length=100, null=True, blank=True)
    accession_identifier = models.CharField(max_length=100, null=True, blank=True)

    status = models.CharField(max_length=100, null=True, blank=True)

    type = models.JSONField(default=dict, null=False, blank=False)

    subject = models.ForeignKey(
        PatientRegistration,
        on_delete=models.CASCADE,
        related_name="specimen",
    )
    request = models.ForeignKey(
        ServiceRequest, on_delete=models.CASCADE, related_name="specimen"
    )

    collected_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="collected_specimen",
    )
    collected_at = models.DateTimeField(null=True, blank=True)

    dispatched_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dispatched_specimen",
    )
    dispatched_at = models.DateTimeField(null=True, blank=True)

    received_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="received_specimen",
    )
    received_at = models.DateTimeField(null=True, blank=True)

    condition = models.JSONField(null=True, blank=True)

    processing = models.JSONField(default=list, null=True, blank=True)

    note = models.JSONField(default=list, null=True, blank=True)

    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
