# Generated by Django 5.0.4 on 2024-04-14 22:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('users', models.CharField(max_length=300)),
                ('adminUsers', models.CharField(max_length=300)),
                ('dateCreated', models.DateTimeField(verbose_name='date created')),
                ('dateLastModified', models.DateTimeField(verbose_name='date last modified')),
            ],
        ),
        migrations.CreateModel(
            name='CaseFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateCreated', models.DateTimeField(verbose_name='date created')),
                ('dateLastModified', models.DateTimeField(verbose_name='date last modified')),
                ('createdBy', models.CharField(max_length=300)),
                ('lastModifiedBy', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('ARCHIVE', 'Archive'), ('LONGTERM MONITOR', 'Longterm Monitor'), ('DECEASED', 'Deceased')], default='ACTIVE', max_length=20)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CaseManagement.organization')),
            ],
        ),
        migrations.CreateModel(
            name='TargetOfInterest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=300)),
                ('middleNames', models.CharField(max_length=300)),
                ('lastName', models.CharField(max_length=300)),
                ('fullName', models.CharField(max_length=300)),
                ('additionalNames', models.CharField(max_length=300)),
                ('dateOfBirth', models.DateTimeField(verbose_name='Date of Birth')),
                ('currentAddress', models.CharField(max_length=300)),
                ('previousAddresses', models.CharField(max_length=300)),
                ('associatedAddresses', models.CharField(max_length=300)),
                ('targetJustification', models.TextField(max_length=1000)),
                ('socialSecurityNumber', models.CharField(max_length=300)),
                ('driversLicenseNumber', models.CharField(max_length=300)),
                ('governmentIssueId', models.CharField(max_length=300)),
                ('additionalIdentifications', models.TextField(max_length=300)),
                ('casefile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CaseManagement.casefile')),
            ],
        ),
    ]
