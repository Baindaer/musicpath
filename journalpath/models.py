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
    learned = models.BooleanField('Learned')
    self_appraisal = models.IntegerField('Self Appraisal')
    difficulty = models.IntegerField('Difficulty')
    note = models.TextField('Notes', max_length=256)

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
    user_id = models.ForeignKey(User, on_delete="models.CASCADE")
    date = models.DateField('Date')
    duration = models.IntegerField('Duration')
    rate = models.IntegerField('Rate')
    emoji = models.CharField('Emotion', max_length=16)


class SubSession(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete="models.CASCADE")
    type = models.CharField('Type', max_length=64)
    catalog = models.ForeignKey('Catalog', on_delete="models.PROTECT")
    detail = models.TextField('Detail', max_length=256)
    tempo = models.IntegerField('Tempo')
    unit = models.CharField('Unit', max_length=32)
    session_id = models.ForeignKey('Session', on_delete="models.PROTECT")




