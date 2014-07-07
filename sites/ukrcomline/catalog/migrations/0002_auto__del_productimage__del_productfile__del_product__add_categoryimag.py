# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'ProductImage'
        db.delete_table(u'catalog_productimage')

        # Deleting model 'ProductFile'
        db.delete_table(u'catalog_productfile')

        # Deleting model 'Product'
        db.delete_table(u'catalog_product')

        # Adding model 'CategoryImage'
        db.create_table(u'catalog_categoryimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['catalog.Category'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['CategoryImage'])

        # Adding model 'CategoryFile'
        db.create_table(u'catalog_categoryfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['catalog.Category'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
        ))
        db.send_create_signal(u'catalog', ['CategoryFile'])

        # Deleting field 'Position.product'
        db.delete_column(u'catalog_position', 'product_id')

        # Adding field 'Position.category'
        db.add_column(u'catalog_position', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='positions', to=orm['catalog.Category']),
                      keep_default=False)

    def backwards(self, orm):
        # Adding model 'ProductImage'
        db.create_table(u'catalog_productimage', (
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['catalog.Product'])),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'catalog', ['ProductImage'])

        # Adding model 'ProductFile'
        db.create_table(u'catalog_productfile', (
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='files', to=orm['catalog.Product'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=250)),
        ))
        db.send_create_signal(u'catalog', ['ProductFile'])

        # Adding model 'Product'
        db.create_table(u'catalog_product', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='products', to=orm['catalog.Category'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'catalog', ['Product'])

        # Deleting model 'CategoryImage'
        db.delete_table(u'catalog_categoryimage')

        # Deleting model 'CategoryFile'
        db.delete_table(u'catalog_categoryfile')


        # User chose to not deal with backwards NULL issues for 'Position.product'
        raise RuntimeError("Cannot reverse this migration. 'Position.product' and its values cannot be restored.")
        # Deleting field 'Position.category'
        db.delete_column(u'catalog_position', 'category_id')

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
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['catalog.Category']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'catalog.categoryfile': {
            'Meta': {'object_name': 'CategoryFile'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['catalog.Category']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '250'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'catalog.categoryimage': {
            'Meta': {'object_name': 'CategoryImage'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': u"orm['catalog.Category']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'})
        },
        u'catalog.position': {
            'Meta': {'object_name': 'Position'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'positions'", 'to': u"orm['catalog.Category']"}),
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