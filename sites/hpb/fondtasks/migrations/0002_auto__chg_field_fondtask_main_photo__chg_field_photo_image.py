# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'FondTask.main_photo'
        db.alter_column('fondtasks_fondtask', 'main_photo', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))

        # Changing field 'Photo.image'
        db.alter_column('fondtasks_photo', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'FondTask.main_photo'
        db.alter_column('fondtasks_fondtask', 'main_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'Photo.image'
        db.alter_column('fondtasks_photo', 'image', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

    models = {
        'fondtasks.fondtask': {
            'Meta': {'object_name': 'FondTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_for_main_photo': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'fondtasks.photo': {
            'Meta': {'ordering': "('-title',)", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fondtasks.FondTask']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        }
    }

    complete_apps = ['fondtasks']
