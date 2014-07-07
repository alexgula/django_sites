# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Author.user'
        db.delete_column(u'photocontest_author', 'user_id')

        # Adding field 'Author.email'
        db.add_column(u'photocontest_author', 'email',
                      self.gf('django.db.models.fields.EmailField')(default='', unique=True, max_length=75),
                      keep_default=False)

        # Adding field 'Author.password'
        db.add_column(u'photocontest_author', 'password',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Adding field 'Author.name'
        db.add_column(u'photocontest_author', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250),
                      keep_default=False)

        # Adding field 'Author.post_date'
        db.add_column(u'photocontest_author', 'post_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 5, 18, 16, 9, 7, 706000), blank=True),
                      keep_default=False)

        # Adding field 'Author.active'
        db.add_column(u'photocontest_author', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Author.user'
        raise RuntimeError("Cannot reverse this migration. 'Author.user' and its values cannot be restored.")
        # Deleting field 'Author.email'
        db.delete_column(u'photocontest_author', 'email')

        # Deleting field 'Author.password'
        db.delete_column(u'photocontest_author', 'password')

        # Deleting field 'Author.name'
        db.delete_column(u'photocontest_author', 'name')

        # Deleting field 'Author.post_date'
        db.delete_column(u'photocontest_author', 'post_date')

        # Deleting field 'Author.active'
        db.delete_column(u'photocontest_author', 'active')

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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['photocontest']