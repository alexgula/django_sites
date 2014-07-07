# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Results.engine'
        db.alter_column('searchbot_results', 'engine', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Results.engine'
        db.alter_column('searchbot_results', 'engine', self.gf('django.db.models.fields.TextField')())

    models = {
        'searchbot.results': {
            'Meta': {'object_name': 'Results'},
            'engine': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'position': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'search': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchbot.Search']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['searchbot.Site']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'searchbot.search': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Search'},
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
