# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Job.content'
        db.delete_column(u'celery_manager_job', 'content')

        # Adding field 'Job.result'
        db.add_column(u'celery_manager_job', 'result',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Job.content'
        db.add_column(u'celery_manager_job', 'content',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Job.result'
        db.delete_column(u'celery_manager_job', 'result')


    models = {
        u'celery_manager.job': {
            'Meta': {'object_name': 'Job'},
            'args': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'timestamp_creazione': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 9, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_modifica': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 9, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['celery_manager']