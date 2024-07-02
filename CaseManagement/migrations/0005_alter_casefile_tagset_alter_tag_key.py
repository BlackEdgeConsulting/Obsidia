# Generated by Django 5.0.4 on 2024-04-21 16:01

import CaseManagement.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0004_tag_remove_casefile_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casefile',
            name='tagSet',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CaseManagement.tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='key',
            field=models.CharField(max_length=300),
        ),
    ]
