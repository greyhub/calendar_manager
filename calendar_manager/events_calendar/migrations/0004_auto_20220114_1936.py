# Generated by Django 2.2.13 on 2022-01-14 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_calendar', '0003_group_groupevent_groupmember'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupevent',
            old_name='tittle',
            new_name='title',
        ),
    ]
