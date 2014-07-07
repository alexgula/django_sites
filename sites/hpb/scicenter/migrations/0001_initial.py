# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table(u'scicenter_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('main_photo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('title_for_main_photo', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal(u'scicenter', ['Page'])

        # Adding model 'Photo'
        db.create_table(u'scicenter_photo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scicenter.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'scicenter', ['Photo'])

    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table(u'scicenter_page')

        # Deleting model 'Photo'
        db.delete_table(u'scicenter_photo')

    models = {
        u'scicenter.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_for_main_photo': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        u'scicenter.photo': {
            'Meta': {'ordering': "('title',)", 'object_name': 'Photo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['scicenter.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['scicenter']