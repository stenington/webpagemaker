# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Page.short_url_id'
        db.add_column('api_page', 'short_url_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Page.short_url_id'
        db.delete_column('api_page', 'short_url_id')

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