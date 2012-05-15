# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

NUMERALS = "3fldc4mzjyqr7bkug5vh0a68xpon9stew12i"

def rebase(num, numerals=NUMERALS):
    base = len(numerals)
    left_digits = num // base
    if left_digits == 0:
        return numerals[num % base]
    else:
        return rebase(left_digits, numerals) + numerals[num % base]

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for page in orm.Page.objects.all():
            page.short_url_id = rebase(page.id)
            page.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        raise RuntimeError("Cannot go back.")

    models = {
        'api.page': {
            'Meta': {'object_name': 'Page'},
            'html': ('django.db.models.fields.TextField', [], {'max_length': '10000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original_url': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'short_url_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['api']
    symmetrical = True
