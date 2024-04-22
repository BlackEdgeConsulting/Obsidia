# Generated by Django 5.0.4 on 2024-04-21 16:03

import CaseManagement.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0005_alter_casefile_tagset_alter_tag_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casefile',
            name='tagSet',
            field=models.ForeignKey(blank=True, default=CaseManagement.models.Tag.get_default_pk, null=True, on_delete=django.db.models.deletion.SET_NULL, to='CaseManagement.tag'),
        ),
    ]
