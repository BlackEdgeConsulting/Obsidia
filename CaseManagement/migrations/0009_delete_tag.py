# Generated by Django 5.0.4 on 2024-06-24 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0008_alter_organization_name_alter_tag_casefile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
