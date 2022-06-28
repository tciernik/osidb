# Generated by Django 3.2.9 on 2021-12-10 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("osidb", "0022_tracker_status_resolution_blank"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="flaw",
            name="is_csaw",
        ),
        migrations.RemoveField(
            model_name="flawevent",
            name="is_csaw",
        ),
        migrations.RemoveField(
            model_name="flawhistory",
            name="is_csaw",
        ),
        migrations.AddField(
            model_name="flaw",
            name="is_major_incident",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="flawevent",
            name="is_major_incident",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name="flawhistory",
            name="is_major_incident",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="flawmeta",
            name="type",
            field=models.CharField(
                choices=[
                    ("ERRATA", "Errata"),
                    ("REFERENCE", "Reference"),
                    ("ACKNOWLEDGMENT", "Acknowledgment"),
                    ("EXPLOIT", "Exploit"),
                    ("MAJOR_INCIDENT", "Major Incident"),
                    ("MAJOR_INCIDENT_LITE", "Major Incident Lite"),
                    ("REQUIRES_DOC_TEXT", "Requires Doc Text"),
                    ("NIST_CVSS_VALIDATION", "Nist Cvss Validation"),
                    ("NEED_INFO", "Need Info"),
                    ("CHECKLIST", "Checklist"),
                    ("NVD_CVSS", "Nvd Cvss"),
                ],
                max_length=500,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="flawmetaevent",
            name="type",
            field=models.CharField(
                choices=[
                    ("ERRATA", "Errata"),
                    ("REFERENCE", "Reference"),
                    ("ACKNOWLEDGMENT", "Acknowledgment"),
                    ("EXPLOIT", "Exploit"),
                    ("MAJOR_INCIDENT", "Major Incident"),
                    ("MAJOR_INCIDENT_LITE", "Major Incident Lite"),
                    ("REQUIRES_DOC_TEXT", "Requires Doc Text"),
                    ("NIST_CVSS_VALIDATION", "Nist Cvss Validation"),
                    ("NEED_INFO", "Need Info"),
                    ("CHECKLIST", "Checklist"),
                    ("NVD_CVSS", "Nvd Cvss"),
                ],
                max_length=500,
                null=True,
            ),
        ),
    ]
