# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Removing unique constraint on 'ExchangeFile', fields ['exchange', 'filename']
        db.delete_unique('exchange1c_exchangefile', ['exchange_id', 'filename'])

        # Deleting model 'ExchangeFile'
        db.delete_table('exchange1c_exchangefile')

        # Adding field 'Exchange.status'
        db.add_column('exchange1c_exchange', 'status', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

    def backwards(self, orm):

        # Adding model 'ExchangeFile'
        db.create_table('exchange1c_exchangefile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('exchange', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['exchange1c.Exchange'])),
        ))
        db.send_create_signal('exchange1c', ['ExchangeFile'])

        # Adding unique constraint on 'ExchangeFile', fields ['exchange', 'filename']
        db.create_unique('exchange1c_exchangefile', ['exchange_id', 'filename'])

        # Deleting field 'Exchange.status'
        db.delete_column('exchange1c_exchange', 'status')

    models = {
        'exchange1c.exchange': {
            'Meta': {'object_name': 'Exchange'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange_type': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
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
