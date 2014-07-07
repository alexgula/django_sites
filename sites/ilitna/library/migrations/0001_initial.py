# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Author'
        db.create_table('library_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('first_name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('family_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('family_name_ru', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('date_born', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('date_died', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('portrait', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('library', ['Author'])

        # Adding model 'Work'
        db.create_table('library_work', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['library.Work'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('listed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('library', ['Work'])

        # Adding M2M table for field authors on 'Work'
        db.create_table('library_work_authors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('work', models.ForeignKey(orm['library.work'], null=False)),
            ('author', models.ForeignKey(orm['library.author'], null=False))
        ))
        db.create_unique('library_work_authors', ['work_id', 'author_id'])

        # Adding model 'Publisher'
        db.create_table('library_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('library', ['Publisher'])

        # Adding model 'Publication'
        db.create_table('library_publication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isbn', self.gf('django.db.models.fields.CharField')(max_length=17, blank=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Work'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Publisher'])),
            ('year', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pages', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('format', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('copies', self.gf('django.db.models.fields.PositiveIntegerField')(blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('library', ['Publication'])

        # Adding model 'WorkText'
        db.create_table('library_work_worktext', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='worktext_set', to=orm['library.Work'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('library', ['WorkText'])

        # Adding model 'WorkImage'
        db.create_table('library_work_workimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=250)),
            ('caption', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workimage_set', to=orm['library.Work'])),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('position', self.gf('django.db.models.fields.CharField')(default='right', max_length=10)),
        ))
        db.send_create_signal('library', ['WorkImage'])

    def backwards(self, orm):
        # Deleting model 'Author'
        db.delete_table('library_author')

        # Deleting model 'Work'
        db.delete_table('library_work')

        # Removing M2M table for field authors on 'Work'
        db.delete_table('library_work_authors')

        # Deleting model 'Publisher'
        db.delete_table('library_publisher')

        # Deleting model 'Publication'
        db.delete_table('library_publication')

        # Deleting model 'WorkText'
        db.delete_table('library_work_worktext')

        # Deleting model 'WorkImage'
        db.delete_table('library_work_workimage')

    models = {
        'library.author': {
            'Meta': {'object_name': 'Author'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'date_born': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'date_died': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'family_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'family_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'first_name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'portrait': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'library.publication': {
            'Meta': {'object_name': 'Publication'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'copies': ('django.db.models.fields.PositiveIntegerField', [], {'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.CharField', [], {'max_length': '17', 'blank': 'True'}),
            'pages': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Publisher']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Work']"}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'library.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        'library.work': {
            'Meta': {'object_name': 'Work'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['library.Author']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'listed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['library.Work']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'library.workimage': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'WorkImage', 'db_table': "'library_work_workimage'"},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '250'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workimage_set'", 'to': "orm['library.Work']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'right'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'library.worktext': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'WorkText', 'db_table': "'library_work_worktext'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'worktext_set'", 'to': "orm['library.Work']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['library']