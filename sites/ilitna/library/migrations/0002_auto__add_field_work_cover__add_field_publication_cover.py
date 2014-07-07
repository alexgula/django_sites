# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Work.cover'
        db.add_column('library_work', 'cover',
                      self.gf('sorl.thumbnail.fields.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Publication.cover'
        db.add_column('library_publication', 'cover',
                      self.gf('sorl.thumbnail.fields.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'Work.cover'
        db.delete_column('library_work', 'cover')

        # Deleting field 'Publication.cover'
        db.delete_column('library_publication', 'cover')

    models = {
        'library.author': {
            'Meta': {'object_name': 'Author'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_born': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_died': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'family_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portrait': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'library.publication': {
            'Meta': {'object_name': 'Publication'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'copies': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'cover': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Publisher']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Work']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'library.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'library.work': {
            'Meta': {'object_name': 'Work'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['library.Author']", 'symmetrical': 'False'}),
            'cover': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['library.Work']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'library.workimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'WorkImage', 'db_table': "'library_work_workimage'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workimage_set'", 'to': "orm['library.Work']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'library.worktext': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'WorkText', 'db_table': "'library_work_worktext'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worktext_set'", 'to': "orm['library.Work']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['library']