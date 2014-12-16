# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0013_collaborator'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='facebook',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='googleplus',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Google+', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='twitter',
            field=models.CharField(max_length=150, null=True, blank=True),
            preserve_default=True,
        ),
    ]
