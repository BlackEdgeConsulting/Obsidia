# Generated by Django 5.0.4 on 2024-07-14 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0014_tagset_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagset',
            name='casefile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='CaseManagement.casefile'),
        ),
    ]
