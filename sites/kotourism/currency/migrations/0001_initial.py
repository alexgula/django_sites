# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Currency'
        db.create_table('currency_currency', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('lang', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=14, decimal_places=2)),
        ))
        db.send_create_signal('currency', ['Currency'])


    def backwards(self, orm):

        # Deleting model 'Currency'
        db.delete_table('currency_currency')


    models = {
        'currency.currency': {
            'Meta': {'object_name': 'Currency'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '14', 'decimal_places': '2'})
        }
    }

    complete_apps = ['currency']
