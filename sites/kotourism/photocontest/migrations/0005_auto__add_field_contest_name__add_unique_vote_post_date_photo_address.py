# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contest.name'
        db.add_column(u'photocontest_contest', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250),
                      keep_default=False)

        # Adding unique constraint on 'Vote', fields ['post_date', 'photo', 'address']
        db.create_unique(u'photocontest_vote', ['post_date', 'photo_id', 'address'])

    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['post_date', 'photo', 'address']
        db.delete_unique(u'photocontest_vote', ['post_date', 'photo_id', 'address'])

        # Deleting field 'Contest.name'
        db.delete_column(u'photocontest_contest', 'name')

    models = {
        u'photocontest.author': {
            'Meta': {'object_name': 'Author'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'photocontest.contest': {
            'Meta': {'object_name': 'Contest'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_from': ('django.db.models.fields.DateTimeField', [], {}),
            'date_to': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'photocontest.photo': {
            'Meta': {'unique_together': "(('active', 'post_date'),)", 'object_name': 'Photo'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocontest.Author']"}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocontest.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'photocontest.vote': {
            'Meta': {'unique_together': "(('photo', 'address', 'post_date'),)", 'object_name': 'Vote'},
            'address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photo': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['photocontest.Photo']"}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['photocontest']