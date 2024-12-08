from django.db import models

from care.emr.models import EMRBaseModel


class Observation(EMRBaseModel):
    status = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    category = models.JSONField(default=dict)
    main_code = models.JSONField(default=dict)
    alternate_coding = models.JSONField(default=list)
    subject_type = models.CharField(max_length=255)
    subject_id = models.UUIDField()
    patient = models.ForeignKey(
        "facility.PatientRegistration", on_delete=models.CASCADE
    )
    encounter = models.ForeignKey(
        "facility.PatientConsultation", on_delete=models.CASCADE
    )
    effective_datetime = models.DateTimeField()
    data_entered_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="observations_entered"
    )
    performer = models.JSONField(default=dict)
    value = models.TextField()
    value_code = models.JSONField(default=dict)
    note = models.TextField()
    body_site = models.JSONField(default=dict)
    method = models.JSONField(default=dict)
    reference_range = models.JSONField(default=list)
    interpretation = models.CharField(max_length=255)
    parent = models.UUIDField(null=True)
    questionnaire_response = models.ForeignKey(
        "emr.QuestionnaireResponse", on_delete=models.CASCADE, null=True
    )
