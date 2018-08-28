# Generated by Django 2.1 on 2018-08-25 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journalpath', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('date', models.DateField(verbose_name='Date added')),
                ('type', models.CharField(max_length=32, verbose_name='Type')),
                ('author', models.ForeignKey(on_delete='models.PROTECT', to='journalpath.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='Date')),
                ('duration', models.IntegerField(verbose_name='Duration')),
                ('rate', models.IntegerField(verbose_name='Rate')),
                ('emoji', models.CharField(max_length=64, verbose_name='Emotion')),
            ],
        ),
        migrations.CreateModel(
            name='SubSession',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=64, verbose_name='Type')),
                ('detail', models.TextField(max_length=256, verbose_name='Detail')),
                ('tempo', models.IntegerField(verbose_name='Tempo')),
                ('unit', models.CharField(max_length=32, verbose_name='Unit')),
                ('catalog', models.ForeignKey(on_delete='models.PROTECT', to='journalpath.Catalog')),
                ('session_id', models.ForeignKey(on_delete='models.PROTECT', to='journalpath.Session')),
            ],
        ),
        migrations.DeleteModel(
            name='Repertory',
        ),
    ]
