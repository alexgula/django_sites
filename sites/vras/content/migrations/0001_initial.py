# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table(u'content_news', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=250, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_on', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'content', ['News'])

        # Adding model 'NewsImage'
        db.create_table(u'content_newsimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['content.News'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'content', ['NewsImage'])

        # Adding model 'StaticPage'
        db.create_table(u'content_staticpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=250, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'content', ['StaticPage'])

        # Adding model 'StaticPageImage'
        db.create_table(u'content_staticpageimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['content.StaticPage'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'content', ['StaticPageImage'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table(u'content_news')

        # Deleting model 'NewsImage'
        db.delete_table(u'content_newsimage')

        # Deleting model 'StaticPage'
        db.delete_table(u'content_staticpage')

        # Deleting model 'StaticPageImage'
        db.delete_table(u'content_staticpageimage')


    models = {
        u'content.news': {
            'Meta': {'object_name': 'News'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'content.newsimage': {
            'Meta': {'object_name': 'NewsImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['content.News']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'})
        },
        u'content.staticpage': {
            'Meta': {'object_name': 'StaticPage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        u'content.staticpageimage': {
            'Meta': {'object_name': 'StaticPageImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['content.StaticPage']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['content']