# Generated by Django 5.0 on 2024-02-25 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('JobBazzar', '0002_delete_userdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_title', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='logos/')),
                ('location', models.CharField(max_length=100)),
                ('current_date', models.DateField()),
                ('hours', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('rate', models.CharField(max_length=100)),
                ('salary', models.CharField(max_length=100)),
                ('job_description', models.TextField()),
                ('key_responsibilities', models.TextField()),
                ('skill', models.TextField()),
                ('experience', models.CharField(max_length=100)),
                ('time', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=100)),
                ('need', models.CharField(max_length=100)),
            ],
        ),
    ]
