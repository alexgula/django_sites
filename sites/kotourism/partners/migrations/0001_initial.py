# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Partner'
        db.create_table(u'partners_partner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('important', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('banner', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'partners', ['Partner'])

    def backwards(self, orm):
        # Deleting model 'Partner'
        db.delete_table(u'partners_partner')

    models = {
        u'partners.partner': {
            'Meta': {'object_name': 'Partner'},
            'banner': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'important': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['partners']