# Generated by Django 4.2.8 on 2024-01-10 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0008_alter_paperinfo_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperinfo',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to='pdfFiles/%Y%m%d/'),
        ),
    ]
