# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Log'
        db.create_table('interop_log', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('results', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('interop', ['Log'])

    def backwards(self, orm):

        # Deleting model 'Log'
        db.delete_table('interop_log')

    models = {
        'interop.log': {
            'Meta': {'object_name': 'Log'},
            'action_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'results': ('django.db.models.fields.TextField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['interop']
