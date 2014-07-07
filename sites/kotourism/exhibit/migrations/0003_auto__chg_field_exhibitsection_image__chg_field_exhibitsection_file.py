# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ExhibitSection.image'
        db.alter_column('exhibit_exhibitsection', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True))

        # Changing field 'ExhibitSection.file'
        db.alter_column('exhibit_exhibitsection', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True))
    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ExhibitSection.image'
        raise RuntimeError("Cannot reverse this migration. 'ExhibitSection.image' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ExhibitSection.file'
        raise RuntimeError("Cannot reverse this migration. 'ExhibitSection.file' and its values cannot be restored.")
    models = {
        'exhibit.exhibit': {
            'Meta': {'object_name': 'Exhibit'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'exhibit.exhibitmap': {
            'Meta': {'object_name': 'ExhibitMap'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exhibit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibit.Exhibit']"}),
            'html': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'exhibit.exhibitpartner': {
            'Meta': {'object_name': 'ExhibitPartner'},
            'exhibit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibit.Exhibit']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'exhibit.exhibitsection': {
            'Meta': {'object_name': 'ExhibitSection'},
            'desc': ('django.db.models.fields.TextField', [], {}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'exhibit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibit.Exhibit']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['exhibit']