# Generated by Django 2.1 on 2018-08-27 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journalpath', '0003_auto_20180827_1400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='catalog',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='subsession',
            old_name='user_id',
            new_name='user',
        ),
    ]