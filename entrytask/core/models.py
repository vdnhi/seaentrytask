# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=70)
    salted_password = models.CharField(max_length=60)

    class Meta:
        db_table = 'user_tab'


class Role(models.Model):
    id = models.BigAutoField(primary_key=True)
    rolename = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = 'role_tab'


class UserRoleMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    role_id = models.BigIntegerField()

    class Meta:
        db_table = 'user_role_tab'
        indexes = [models.Index(fields=['user_id'])]


class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    start_date = models.PositiveIntegerField()
    end_date = models.PositiveIntegerField()
    create_uid = models.BigIntegerField()
    create_time = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField()
    location = models.CharField(max_length=100, null=True)
    channel = models.CharField(max_length=50)
    image_url = models.CharField(max_length=100)

    class Meta:
        db_table = 'event_tab'
        ordering = ['id']
        indexes = [models.Index(fields=['id', 'channel'])]


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    content = models.CharField(max_length=255)
    create_time = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField()

    class Meta:
        db_table = 'comment_tab'
        indexes = [models.Index(fields=['event_id'])]


class Like(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()

    class Meta:
        db_table = 'like_tab'
        indexes = [models.Index(fields=['event_id'])]


class Participation(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()
    event_id = models.BigIntegerField()
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = 'participation_tab'
        indexes = [models.Index(fields=['event_id'])]
