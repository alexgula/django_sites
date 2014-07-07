# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('content_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('content', ['News'])

        # Adding model 'InfoPage'
        db.create_table('content_infopage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['content.InfoPage'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('content', ['InfoPage'])

        # Adding model 'GalleryPage'
        db.create_table('content_gallerypage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('title_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('title_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('content', ['GalleryPage'])

        # Adding model 'NewsText'
        db.create_table('content_news_newstext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='newstext_set', to=orm['content.News'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('content', ['NewsText'])

        # Adding model 'NewsImage'
        db.create_table('content_news_newsimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('caption_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('caption_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='newsimage_set', to=orm['content.News'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.CharField')(default='right', max_length=10)),
        ))
        db.send_create_signal('content', ['NewsImage'])

        # Adding model 'InfoPageText'
        db.create_table('content_infopage_infopagetext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='infopagetext_set', to=orm['content.InfoPage'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('content', ['InfoPageText'])

        # Adding model 'InfoPageImage'
        db.create_table('content_infopage_infopageimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('caption_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('caption_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='infopageimage_set', to=orm['content.InfoPage'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.CharField')(default='right', max_length=10)),
        ))
        db.send_create_signal('content', ['InfoPageImage'])

        # Adding model 'GalleryPageImage'
        db.create_table('content_gallerypage_gallerypageimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('caption_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('caption_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gallerypageimage_set', to=orm['content.GalleryPage'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.CharField')(default='right', max_length=10)),
        ))
        db.send_create_signal('content', ['GalleryPageImage'])

    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('content_news')

        # Deleting model 'InfoPage'
        db.delete_table('content_infopage')

        # Deleting model 'GalleryPage'
        db.delete_table('content_gallerypage')

        # Deleting model 'NewsText'
        db.delete_table('content_news_newstext')

        # Deleting model 'NewsImage'
        db.delete_table('content_news_newsimage')

        # Deleting model 'InfoPageText'
        db.delete_table('content_infopage_infopagetext')

        # Deleting model 'InfoPageImage'
        db.delete_table('content_infopage_infopageimage')

        # Deleting model 'GalleryPageImage'
        db.delete_table('content_gallerypage_gallerypageimage')

    models = {
        'content.gallerypage': {
            'Meta': {'ordering': "['title']", 'object_name': 'GalleryPage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'content.gallerypageimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'GalleryPageImage', 'db_table': "'content_gallerypage_gallerypageimage'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'caption_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'caption_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gallerypageimage_set'", 'to': "orm['content.GalleryPage']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'content.infopage': {
            'Meta': {'object_name': 'InfoPage'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['content.InfoPage']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'content.infopageimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InfoPageImage', 'db_table': "'content_infopage_infopageimage'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'caption_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'caption_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'infopageimage_set'", 'to': "orm['content.InfoPage']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'content.infopagetext': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'InfoPageText', 'db_table': "'content_infopage_infopagetext'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'infopagetext_set'", 'to': "orm['content.InfoPage']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'content.news': {
            'Meta': {'ordering': "['-pub_date']", 'object_name': 'News'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'title_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'title_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'})
        },
        'content.newsimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NewsImage', 'db_table': "'content_news_newsimage'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'caption_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'caption_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newsimage_set'", 'to': "orm['content.News']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'content.newstext': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'NewsText', 'db_table': "'content_news_newstext'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'newstext_set'", 'to': "orm['content.News']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['content']