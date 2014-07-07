# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NewsImageContent.size'
        db.add_column(u'content_news_newsimagecontent', 'size',
                      self.gf('django.db.models.fields.CharField')(default='270', max_length=20),
                      keep_default=False)

        # Adding field 'StaticPageImageContent.size'
        db.add_column(u'content_staticpage_staticpageimagecontent', 'size',
                      self.gf('django.db.models.fields.CharField')(default='270', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NewsImageContent.size'
        db.delete_column(u'content_news_newsimagecontent', 'size')

        # Deleting field 'StaticPageImageContent.size'
        db.delete_column(u'content_staticpage_staticpageimagecontent', 'size')


    models = {
        u'content.news': {
            'Meta': {'object_name': 'News'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'content.newsfilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NewsFileContent', 'db_table': "u'content_news_newsfilecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsfilecontent_set'", 'to': u"orm['content.News']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.newsimagecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NewsImageContent', 'db_table': "u'content_news_newsimagecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsimagecontent_set'", 'to': u"orm['content.News']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'270'", 'max_length': '20'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'content.newsrestructuredcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NewsRestructuredContent', 'db_table': "u'content_news_newsrestructuredcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsrestructuredcontent_set'", 'to': u"orm['content.News']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'content.staticpage': {
            'Meta': {'object_name': 'StaticPage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'content.staticpagefilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'StaticPageFileContent', 'db_table': "u'content_staticpage_staticpagefilecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staticpagefilecontent_set'", 'to': u"orm['content.StaticPage']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.staticpageimagecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'StaticPageImageContent', 'db_table': "u'content_staticpage_staticpageimagecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staticpageimagecontent_set'", 'to': u"orm['content.StaticPage']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'270'", 'max_length': '20'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'content.staticpagerestructuredcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'StaticPageRestructuredContent', 'db_table': "u'content_staticpage_staticpagerestructuredcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staticpagerestructuredcontent_set'", 'to': u"orm['content.StaticPage']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['content']