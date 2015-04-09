# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Job.timestamp_prerun'
        db.add_column(u'celery_manager_job', 'timestamp_prerun',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Job.timestamp_postrun'
        db.add_column(u'celery_manager_job', 'timestamp_postrun',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Job.timestamp_prerun'
        db.delete_column(u'celery_manager_job', 'timestamp_prerun')

        # Deleting field 'Job.timestamp_postrun'
        db.delete_column(u'celery_manager_job', 'timestamp_postrun')


    models = {
        u'celery_manager.job': {
            'Meta': {'object_name': 'Job'},
            'args': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "u'MISC'", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'timestamp_creazione': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 8, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_modifica': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 8, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_postrun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_prerun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['celery_manager']