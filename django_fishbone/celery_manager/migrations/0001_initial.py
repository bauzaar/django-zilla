# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'celery_manager_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp_creazione', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 4, 0, 0), auto_now_add=True, db_index=True, blank=True)),
            ('timestamp_modifica', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 4, 0, 0), auto_now=True, db_index=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('task', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('task_id', self.gf('django.db.models.fields.CharField')(max_length=36, db_index=True)),
            ('args', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('kwargs', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'celery_manager', ['Job'])


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'celery_manager_job')


    models = {
        u'celery_manager.job': {
            'Meta': {'object_name': 'Job'},
            'args': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'db_index': 'True'}),
            'timestamp_creazione': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 4, 0, 0)', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'timestamp_modifica': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 4, 0, 0)', 'auto_now': 'True', 'db_index': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['celery_manager']