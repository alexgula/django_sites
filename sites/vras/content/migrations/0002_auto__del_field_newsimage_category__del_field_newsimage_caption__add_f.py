# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'NewsImage.category'
        db.delete_column(u'content_newsimage', 'category_id')

        # Deleting field 'NewsImage.caption'
        db.delete_column(u'content_newsimage', 'caption')

        # Adding field 'NewsImage.parent'
        db.add_column(u'content_newsimage', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='images', to=orm['content.News']),
                      keep_default=False)

        # Deleting field 'StaticPageImage.category'
        db.delete_column(u'content_staticpageimage', 'category_id')

        # Deleting field 'StaticPageImage.caption'
        db.delete_column(u'content_staticpageimage', 'caption')

        # Adding field 'StaticPageImage.parent'
        db.add_column(u'content_staticpageimage', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='images', to=orm['content.StaticPage']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'NewsImage.category'
        raise RuntimeError("Cannot reverse this migration. 'NewsImage.category' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'NewsImage.category'
        db.add_column(u'content_newsimage', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['content.News']),
                      keep_default=False)

        # Adding field 'NewsImage.caption'
        db.add_column(u'content_newsimage', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Deleting field 'NewsImage.parent'
        db.delete_column(u'content_newsimage', 'parent_id')


        # User chose to not deal with backwards NULL issues for 'StaticPageImage.category'
        raise RuntimeError("Cannot reverse this migration. 'StaticPageImage.category' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'StaticPageImage.category'
        db.add_column(u'content_staticpageimage', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['content.StaticPage']),
                      keep_default=False)

        # Adding field 'StaticPageImage.caption'
        db.add_column(u'content_staticpageimage', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, blank=True),
                      keep_default=False)

        # Deleting field 'StaticPageImage.parent'
        db.delete_column(u'content_staticpageimage', 'parent_id')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['content.News']"})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['content.StaticPage']"})
        }
    }

    complete_apps = ['content']