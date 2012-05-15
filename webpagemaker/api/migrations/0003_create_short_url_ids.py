# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."

        from ..models import rebase
        for user in orm.Page.objects.all():
            user.short_url_id = rebase(user.id)
            user.save()

    def backwards(self, orm):
        "Write your backwards methods here."

        for user in orm.Page.objects.all():
            user.short_url_id = ''
            user.save()

    models = {
        'api.page': {
            'Meta': {'object_name': 'Page'},
            'html': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'short_url_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['api']
    symmetrical = True
