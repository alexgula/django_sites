# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Book'
        db.create_table('books_book', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('preamble', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('books', ['Book'])

        # Adding model 'Part'
        db.create_table('books_part', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('in_book', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['books.Book'])),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=150)),
            ('page_num', self.gf('django.db.models.fields.IntegerField')()),
            ('level', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('books', ['Part'])

    def backwards(self, orm):

        # Deleting model 'Book'
        db.delete_table('books_book')

        # Deleting model 'Part'
        db.delete_table('books_part')

    models = {
        'books.book': {
            'Meta': {'ordering': "('author', 'title')", 'object_name': 'Book'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preamble': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'books.part': {
            'Meta': {'ordering': "('in_book', 'page_num', 'order')", 'object_name': 'Part'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_book': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['books.Book']"}),
            'level': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'page_num': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['books']
