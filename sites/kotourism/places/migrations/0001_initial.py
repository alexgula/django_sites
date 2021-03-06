# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Place'
        db.create_table('places_place', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('address_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('phone_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('timetable', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('timetable_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('timetable_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('timetable_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['places.Place'])),
            ('code', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('places', ['Place'])


    def backwards(self, orm):

        # Deleting model 'Place'
        db.delete_table('places_place')


    models = {
        'places.place': {
            'Meta': {'object_name': 'Place'},
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['places.Place']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'timetable': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'timetable_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timetable_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'timetable_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['places']
