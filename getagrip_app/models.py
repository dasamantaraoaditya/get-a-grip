from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django import forms


# Create your models here.

class tasks_log(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE)
    maintask = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    deadline = models.DateTimeField(default=datetime.now)
    date = models.DateTimeField(default=datetime.now)
    todo = 'todo'
    inprogress = 'inprogress'
    needhelp = 'needhelp'
    review = 'review'
    improvements = 'improvements'
    closed = 'closed'
    STATE_CHOISES = (
        (todo, 'To-Do'),
        (inprogress, 'In-Progress'),
        (needhelp, 'Need-Help'),
        (review, 'Review'),
        (improvements, 'Improvements'),
        (closed, 'Closed'),
    )
    state = models.CharField(max_length=20,
                             choices=STATE_CHOISES,
                             default=todo,
                             )
    Maintask = 'MainTask'
    epictask = 'EpicTask'
    generaltask = 'GeneralTask'
    subtask = 'SubTask'
    minitask = 'MiniTask'
    TYPE_CHOISES = (
        (Maintask, 'Main-Task'),
        (epictask, 'Epic-Task'),
        (generaltask, 'General-Task'),
        (subtask, 'Sub-Task'),
        (minitask, 'Mini-Task'),
    )
    type = models.CharField(max_length=20,
                            choices=TYPE_CHOISES,
                            default=maintask,
                            )

    def __unicode__(self):
        return self.title


class comments_log(models.Model):
    task = models.ForeignKey(tasks_log, default=None)
    commented_by = models.ForeignKey(User)
    date = models.DateTimeField(default=datetime.now)
    comment = models.CharField(max_length=150)

    def __unicode__(self):
        return self.comment


class assignees_log(models.Model):
    task = models.ForeignKey(tasks_log, default=None)
    assigneed_to = models.ForeignKey(User, default=None)
    date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return str(self.date)
