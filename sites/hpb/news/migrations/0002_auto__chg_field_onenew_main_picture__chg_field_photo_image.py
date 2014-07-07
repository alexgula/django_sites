# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OneNew.main_picture'
        db.alter_column('news_onenew', 'main_picture', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))

        # Changing field 'Photo.image'
        db.alter_column('news_photo', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'OneNew.main_picture'
        db.alter_column('news_onenew', 'main_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'Photo.image'
        db.alter_column('news_photo', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        'news.onenew': {
            'Meta': {'ordering': "('-published_date',)", 'object_name': 'OneNew'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_picture': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'preview': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_for_main_picture': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'news.photo': {
            'Meta': {'ordering': "('-title',)", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.OneNew']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['news']
