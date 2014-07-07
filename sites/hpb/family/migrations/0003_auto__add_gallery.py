# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Gallery'
        db.create_table('family_gallery', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('family', ['Gallery'])

    def backwards(self, orm):
        # Deleting model 'Gallery'
        db.delete_table('family_gallery')

    models = {
        'family.familymember': {
            'Meta': {'ordering': "('surname',)", 'object_name': 'FamilyMember'},
            'autor_of_citation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'citation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'died_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_portrait': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'preview': ('django.db.models.fields.TextField', [], {}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title_for_main_portrait': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'family.gallery': {
            'Meta': {'object_name': 'Gallery'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'family.picture': {
            'Meta': {'object_name': 'Picture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['family.FamilyMember']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['family']