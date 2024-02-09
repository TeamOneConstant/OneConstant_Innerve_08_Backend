# Generated by Django 4.2.8 on 2024-02-09 07:07

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalReports',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=16)),
                ('document_url', models.FileField(blank=True, null=True, upload_to='medical_reports')),
                ('added_by', models.CharField(blank=True, max_length=32, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('doctor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor_app.doctordetails')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DiseaseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disease', models.CharField(blank=True, max_length=512, null=True)),
                ('description', models.TextField(blank=True, max_length=1024, null=True)),
                ('first_aid', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=512), blank=True, null=True, size=30)),
                ('medicines', models.JSONField(blank=True, max_length=2048, null=True)),
                ('symptoms', models.TextField(max_length=1024)),
                ('text_response', models.TextField(blank=True, max_length=2048, null=True)),
                ('json_response', models.TextField(blank=True, max_length=2048, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
