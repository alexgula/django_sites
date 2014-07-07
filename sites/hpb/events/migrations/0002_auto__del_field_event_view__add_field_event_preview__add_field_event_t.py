# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting field 'Event.view'
        db.delete_column('events_event', 'view')

        # Adding field 'Event.preview'
        db.add_column('events_event', 'preview', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True), keep_default=False)

        # Adding field 'Event.text'
        db.add_column('events_event', 'text', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Event.view'
        raise RuntimeError("Cannot reverse this migration. 'Event.view' and its values cannot be restored.")

        # Deleting field 'Event.preview'
        db.delete_column('events_event', 'preview')

        # Deleting field 'Event.text'
        db.delete_column('events_event', 'text')

    models = {
        'events.event': {
            'Meta': {'ordering': "('-start_date',)", 'object_name': 'Event'},
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'end_time': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'preview': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'start_time': ('django.db.models.fields.TimeField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['events']
