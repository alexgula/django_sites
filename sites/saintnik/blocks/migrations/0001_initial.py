# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TextBlock'
        db.create_table('blocks_textblock', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('blocks', ['TextBlock'])

    def backwards(self, orm):
        # Deleting model 'TextBlock'
        db.delete_table('blocks_textblock')

    models = {
        'blocks.textblock': {
            'Meta': {'ordering': "('code',)", 'object_name': 'TextBlock'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['blocks']