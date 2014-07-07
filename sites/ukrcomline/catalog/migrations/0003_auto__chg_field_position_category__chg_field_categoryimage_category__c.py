# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Position.category'
        db.alter_column(u'catalog_position', 'category_id', self.gf('mptt.fields.TreeForeignKey')(to=orm['catalog.Category']))

        # Changing field 'CategoryImage.category'
        db.alter_column(u'catalog_categoryimage', 'category_id', self.gf('mptt.fields.TreeForeignKey')(to=orm['catalog.Category']))
        # Adding M2M table for field more_parents on 'Category'
        db.create_table(u'catalog_category_more_parents', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_category', models.ForeignKey(orm[u'catalog.category'], null=False)),
            ('to_category', models.ForeignKey(orm[u'catalog.category'], null=False))
        ))
        db.create_unique(u'catalog_category_more_parents', ['from_category_id', 'to_category_id'])


        # Changing field 'CategoryFile.category'
        db.alter_column(u'catalog_categoryfile', 'category_id', self.gf('mptt.fields.TreeForeignKey')(to=orm['catalog.Category']))
    def backwards(self, orm):

        # Changing field 'Position.category'
        db.alter_column(u'catalog_position', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category']))

        # Changing field 'CategoryImage.category'
        db.alter_column(u'catalog_categoryimage', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category']))
        # Removing M2M table for field more_parents on 'Category'
        db.delete_table('catalog_category_more_parents')


        # Changing field 'CategoryFile.category'
        db.alter_column(u'catalog_categoryfile', 'category_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Category']))
    models = {
        u'catalog.category': {
            'Meta': {'object_name': 'Category'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'more_parents': ('mptt.fields.TreeManyToManyField', [], {'blank': 'True', 'related_name': "'more_parents_rel_+'", 'null': 'True', 'to': u"orm['catalog.Category']"}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['catalog.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'catalog.categoryfile': {
            'Meta': {'object_name': 'CategoryFile'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'related_name': "'files'", 'to': u"orm['catalog.Category']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalog.categoryimage': {
            'Meta': {'object_name': 'CategoryImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('mptt.fields.TreeForeignKey', [], {'related_name': "'images'", 'to': u"orm['catalog.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'})
        },
        u'catalog.position': {
            'Meta': {'object_name': 'Position'},
            'category': ('mptt.fields.TreeForeignKey', [], {'related_name': "'positions'", 'to': u"orm['catalog.Category']"}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'positions'", 'to': u"orm['catalog.PositionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'catalog.positiongroup': {
            'Meta': {'object_name': 'PositionGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        }
    }

    complete_apps = ['catalog']