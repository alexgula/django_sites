# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Exchange'
        db.create_table('exchange1c_exchange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('date_start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('exchange1c', ['Exchange'])

        # Adding model 'ExchangeLog'
        db.create_table('exchange1c_exchangelog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exchange', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange1c.Exchange'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('date_log', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('exchange1c', ['ExchangeLog'])

        # Adding model 'ExchangeFile'
        db.create_table('exchange1c_exchangefile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('exchange', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange1c.Exchange'])),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('exchange1c', ['ExchangeFile'])

        # Adding unique constraint on 'ExchangeFile', fields ['exchange', 'filename']
        db.create_unique('exchange1c_exchangefile', ['exchange_id', 'filename'])

    def backwards(self, orm):

        # Removing unique constraint on 'ExchangeFile', fields ['exchange', 'filename']
        db.delete_unique('exchange1c_exchangefile', ['exchange_id', 'filename'])

        # Deleting model 'Exchange'
        db.delete_table('exchange1c_exchange')

        # Deleting model 'ExchangeLog'
        db.delete_table('exchange1c_exchangelog')

        # Deleting model 'ExchangeFile'
        db.delete_table('exchange1c_exchangefile')

    models = {
        'exchange1c.exchange': {
            'Meta': {'object_name': 'Exchange'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'exchange1c.exchangefile': {
            'Meta': {'unique_together': "(('exchange', 'filename'),)", 'object_name': 'ExchangeFile'},
            'exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exchange1c.Exchange']"}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'exchange1c.exchangelog': {
            'Meta': {'object_name': 'ExchangeLog'},
            'date_log': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exchange1c.Exchange']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '1024'})
        }
    }

    complete_apps = ['exchange1c']
