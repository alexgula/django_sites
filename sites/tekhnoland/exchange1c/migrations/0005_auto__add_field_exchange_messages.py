# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Exchange.messages'
        db.add_column('exchange1c_exchange', 'messages', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

    def backwards(self, orm):

        # Deleting field 'Exchange.messages'
        db.delete_column('exchange1c_exchange', 'messages')

    models = {
        'exchange1c.exchange': {
            'Meta': {'ordering': "('-date_start',)", 'object_name': 'Exchange'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'date_start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange_type': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'messages': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'exchange1c.exchangelog': {
            'Meta': {'object_name': 'ExchangeLog'},
            'date_log': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exchange1c.Exchange']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['exchange1c']
