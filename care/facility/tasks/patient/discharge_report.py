import datetime
import random
import string
import time
from uuid import uuid4 as uuid

import boto3
import celery
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import make_aware
from hardcopy import bytestring_to_pdf

from care.facility.models import (
    DailyRound,
    Disease,
    DiseaseStatusEnum,
    InvestigationValue,
    PatientConsultation,
    PatientRegistration,
    PatientSample,
)
from care.utils.csp import config as cs_provider


def randomString(stringLength):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for i in range(stringLength))


@celery.task()
def generate_discharge_report(patient_id, email=None, save=False):
    patient = PatientRegistration.objects.get(id=patient_id)
    consultations = PatientConsultation.objects.filter(patient=patient).order_by(
        "-created_date"
    )
    diseases = Disease.objects.filter(patient=patient)
    if consultations.exists():
        consultation = consultations.first()
        samples = PatientSample.objects.filter(
            patient=patient, consultation=consultation
        )
        daily_rounds = DailyRound.objects.filter(consultation=consultation)
        investigations = InvestigationValue.objects.filter(consultation=consultation.id)
        investigations = list(
            filter(
                lambda inv: inv.value is not None or inv.notes is not None,
                investigations,
            )
        )
    else:
        consultation = None
        samples = None
        daily_rounds = None
        investigations = None
    date = make_aware(datetime.datetime.now())
    disease_status = DiseaseStatusEnum(patient.disease_status).name.capitalize()
    html_string = render_to_string(
        "reports/patient_pdf_report.html",
        {
            "patient": patient,
            "samples": samples,
            "consultation": consultation,
            "consultations": consultations,
            "dailyrounds": daily_rounds,
            "date": date,
            "diseases": diseases,
            "investigations": investigations,
            "disease_status": disease_status,
        },
    )
    filename = str(int(round(time.time() * 1000))) + randomString(10) + ".pdf"
    bytestring_to_pdf(
        html_string.encode(),
        default_storage.open(filename, "w+"),
        **{
            "no-margins": None,
            "disable-gpu": None,
            "disable-dev-shm-usage": False,
            "window-size": "2480,3508",
        },
    )
    file = default_storage.open(filename, "rb")

    if email:
        msg = EmailMessage(
            "Patient Discharge Summary",
            "Please find the attached file",
            settings.DEFAULT_FROM_EMAIL,
            (email,),
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.attach(
            patient.name + "-Discharge_Summary.pdf", file.read(), "application/pdf"
        )
        msg.send()

    if save:
        s3 = boto3.client(
            "s3",
            **cs_provider.get_client_config(),
        )
        image_location = f"discharge_summary/{uuid()}.pdf"
        s3.put_object(
            Bucket=settings.FILE_UPLOAD_BUCKET,
            Key=image_location,
            Body=file,
        )
        signed_url = s3.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": settings.FILE_UPLOAD_BUCKET,
                "Key": image_location,
            },
            ExpiresIn=60 * 60 * 24 * 2,  # 2 days
        )

    default_storage.delete(filename)
    return signed_url if save else None
