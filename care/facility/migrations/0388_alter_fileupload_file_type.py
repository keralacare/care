# Generated by Django 4.2.2 on 2023-10-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("facility", "0387_merge_20230911_2303"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileupload",
            name="file_type",
            field=models.IntegerField(
                choices=[
                    (1, "PATIENT"),
                    (2, "CONSULTATION"),
                    (3, "SAMPLE_MANAGEMENT"),
                    (4, "CLAIM"),
                    (5, "DISCHARGE_SUMMARY"),
                    (6, "COMMUNICATION"),
                    (7, "ABDM_HEALTH_INFORMATION"),
                ],
                default=1,
            ),
        ),
    ]
