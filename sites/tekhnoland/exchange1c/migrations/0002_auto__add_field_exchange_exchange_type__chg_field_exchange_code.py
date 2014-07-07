# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Exchange.exchange_type'
        db.add_column('exchange1c_exchange', 'exchange_type', self.gf('django.db.models.fields.CharField')(default='catalog', max_length=7), keep_default=False)

        # Changing field 'Exchange.code'
        db.alter_column('exchange1c_exchange', 'code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40))

    def backwards(self, orm):

        # Deleting field 'Exchange.exchange_type'
        db.delete_column('exchange1c_exchange', 'exchange_type')

        # Changing field 'Exchange.code'
        db.alter_column('exchange1c_exchange', 'code', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True))

    models = {
        'exchange1c.exchange': {
            'Meta': {'object_name': 'Exchange'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange_type': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
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
