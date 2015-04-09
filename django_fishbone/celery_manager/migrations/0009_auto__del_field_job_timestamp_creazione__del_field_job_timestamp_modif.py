# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Job.timestamp_creazione'
        db.delete_column(u'celery_manager_job', 'timestamp_creazione')

        # Deleting field 'Job.timestamp_modifica'
        db.delete_column(u'celery_manager_job', 'timestamp_modifica')

        # Adding field 'Job.timestamp_created'
        db.add_column(u'celery_manager_job', 'timestamp_created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 3, 30, 0, 0), auto_now_add=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Job.timestamp_modified'
        db.add_column(u'celery_manager_job', 'timestamp_modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 3, 30, 0, 0), auto_now=True, db_index=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Job.timestamp_creazione'
        db.add_column(u'celery_manager_job', 'timestamp_creazione',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 12, 0, 0), auto_now_add=True, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Job.timestamp_modifica'
        db.add_column(u'celery_manager_job', 'timestamp_modifica',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 12, 0, 0), auto_now=True, blank=True, db_index=True),
                      keep_default=False)

        # Deleting field 'Job.timestamp_created'
        db.delete_column(u'celery_manager_job', 'timestamp_created')

        # Deleting field 'Job.timestamp_modified'
        db.delete_column(u'celery_manager_job', 'timestamp_modified')


    models = {
        u'celery_manager.job': {
            'Meta': {'object_name': 'Job'},
            'args': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "u'MISC'", 'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'PENDING'", 'max_length': '10'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'task_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'db_index': 'True'}),
            'timestamp_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 30, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 30, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_postrun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'timestamp_prerun': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['celery_manager']