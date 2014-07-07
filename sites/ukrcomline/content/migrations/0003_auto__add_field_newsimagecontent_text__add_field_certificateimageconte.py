# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'NewsImageContent.text'
        db.add_column(u'content_news_newsimagecontent', 'text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'CertificateImageContent.text'
        db.add_column(u'content_certificate_certificateimagecontent', 'text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


        # Changing field 'Portfolio.created_on'
        db.alter_column(u'content_portfolio', 'created_on', self.gf('django.db.models.fields.DateTimeField')())
        # Adding field 'PortfolioImageContent.text'
        db.add_column(u'content_portfolio_portfolioimagecontent', 'text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'StaticPageImageContent.text'
        db.add_column(u'content_staticpage_staticpageimagecontent', 'text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'NewsImageContent.text'
        db.delete_column(u'content_news_newsimagecontent', 'text')

        # Deleting field 'CertificateImageContent.text'
        db.delete_column(u'content_certificate_certificateimagecontent', 'text')


        # Changing field 'Portfolio.created_on'
        db.alter_column(u'content_portfolio', 'created_on', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))
        # Deleting field 'PortfolioImageContent.text'
        db.delete_column(u'content_portfolio_portfolioimagecontent', 'text')

        # Deleting field 'StaticPageImageContent.text'
        db.delete_column(u'content_staticpage_staticpageimagecontent', 'text')


    models = {
        u'content.certificate': {
            'Meta': {'object_name': 'Certificate'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'content.certificatefilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'CertificateFileContent', 'db_table': "u'content_certificate_certificatefilecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificatefilecontent_set'", 'to': u"orm['content.Certificate']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.certificateimagecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'CertificateImageContent', 'db_table': "u'content_certificate_certificateimagecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificateimagecontent_set'", 'to': u"orm['content.Certificate']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'content.certificaterestructuredcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'CertificateRestructuredContent', 'db_table': "u'content_certificate_certificaterestructuredcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'certificaterestructuredcontent_set'", 'to': u"orm['content.Certificate']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
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
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsimagecontent_set'", 'to': u"orm['content.News']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        u'content.portfolio': {
            'Meta': {'object_name': 'Portfolio'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '255'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'content.portfoliofilecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PortfolioFileContent', 'db_table': "u'content_portfolio_portfoliofilecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portfoliofilecontent_set'", 'to': u"orm['content.Portfolio']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.portfolioimagecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PortfolioImageContent', 'db_table': "u'content_portfolio_portfolioimagecontent'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portfolioimagecontent_set'", 'to': u"orm['content.Portfolio']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'})
        },
        u'content.portfoliorestructuredcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'PortfolioRestructuredContent', 'db_table': "u'content_portfolio_portfoliorestructuredcontent'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'portfoliorestructuredcontent_set'", 'to': u"orm['content.Portfolio']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'content.staticpage': {
            'Meta': {'object_name': 'StaticPage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
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
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'staticpageimagecontent_set'", 'to': u"orm['content.StaticPage']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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