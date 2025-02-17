# Generated by Django 5.0.4 on 2024-07-03 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CaseManagement', '0009_delete_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='dateCreated',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='dateLastModified',
            field=models.DateTimeField(auto_now=True, verbose_name='date last modified'),
        ),
    ]
