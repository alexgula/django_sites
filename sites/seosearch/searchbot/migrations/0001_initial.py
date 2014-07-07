# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Site'
        db.create_table('searchbot_site', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site_domain', self.gf('django.db.models.fields.CharField')(max_length=350)),
            ('keywords', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('searchbot', ['Site'])

        # Adding model 'Search'
        db.create_table('searchbot_search', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('searchbot', ['Search'])

        # Adding model 'Results'
        db.create_table('searchbot_results', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchbot.Site'])),
            ('search', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['searchbot.Search'])),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('engine', self.gf('django.db.models.fields.TextField')()),
            ('position', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal('searchbot', ['Results'])

    def backwards(self, orm):
        # Deleting model 'Site'
        db.delete_table('searchbot_site')

        # Deleting model 'Search'
        db.delete_table('searchbot_search')

        # Deleting model 'Results'
        db.delete_table('searchbot_results')

    models = {
        'searchbot.results': {
            'Meta': {'object_name': 'Results'},
            'engine': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchbot.Search']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchbot.Site']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'searchbot.search': {
            'Meta': {'object_name': 'Search'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'searchbot.site': {
            'Meta': {'object_name': 'Site'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {}),
            'site_domain': ('django.db.models.fields.CharField', [], {'max_length': '350'})
        }
    }

    complete_apps = ['searchbot']