# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'FondTask'
        db.create_table('fondtasks_fondtask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('main_photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title_for_main_photo', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('fondtasks', ['FondTask'])

        # Adding model 'Photo'
        db.create_table('fondtasks_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fondtasks.FondTask'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('fondtasks', ['Photo'])

    def backwards(self, orm):

        # Deleting model 'FondTask'
        db.delete_table('fondtasks_fondtask')

        # Deleting model 'Photo'
        db.delete_table('fondtasks_photo')

    models = {
        'fondtasks.fondtask': {
            'Meta': {'object_name': 'FondTask'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_for_main_photo': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'fondtasks.photo': {
            'Meta': {'ordering': "('-title',)", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['fondtasks.FondTask']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['fondtasks']
