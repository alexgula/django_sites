# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'OneNew'
        db.create_table('news_onenew', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('published_date', self.gf('django.db.models.fields.DateField')()),
            ('preview', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('main_picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title_for_main_picture', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('news', ['OneNew'])

        # Adding model 'Photo'
        db.create_table('news_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['news.OneNew'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('news', ['Photo'])

    def backwards(self, orm):

        # Deleting model 'OneNew'
        db.delete_table('news_onenew')

        # Deleting model 'Photo'
        db.delete_table('news_photo')

    models = {
        'news.onenew': {
            'Meta': {'ordering': "('-published_date',)", 'object_name': 'OneNew'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'preview': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'title_for_main_picture': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'news.photo': {
            'Meta': {'ordering': "('-title',)", 'object_name': 'Photo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'news': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['news.OneNew']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['news']
