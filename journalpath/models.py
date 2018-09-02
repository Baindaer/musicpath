# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Catalog(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    name = models.CharField('Name', max_length=64)
    author = models.ForeignKey('Author', on_delete="models.PROTECT")
    date = models.DateField('Date added')
    type = models.CharField('Type', max_length=32)
    self_appraisal = models.IntegerField('Self Appraisal')
    difficulty = models.IntegerField('Difficulty')
    note = models.TextField('Notes', max_length=256, null=True, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    name = models.CharField('Name', max_length=64)

    def __str__(self):
        return self.name


class Session(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    date = models.DateField('Date')
    duration = models.IntegerField('Duration')
    rate = models.IntegerField('Rate')
    emoji = models.CharField('Emotion', max_length=16, null=True, blank=True)
    type = models.CharField('Type', max_length=64)
    catalog = models.ForeignKey('Catalog', on_delete="models.PROTECT")
    detail = models.TextField('Detail', max_length=256, null=True, blank=True)
    tempo_min = models.IntegerField('Tempo Min', null=True, blank=True)
    tempo_max = models.IntegerField('Tempo Max', null=True, blank=True)
    unit = models.CharField('Unit', max_length=32, null=True, blank=True)

    def __str__(self):
        return str(self.date) + ' ' + self.catalog.name





