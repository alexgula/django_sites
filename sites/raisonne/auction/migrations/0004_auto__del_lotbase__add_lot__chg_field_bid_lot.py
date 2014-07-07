# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Deleting model 'LotBase'
        db.delete_table('auction_lotbase')

        # Adding model 'Lot'
        db.create_table('auction_lot', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('start_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('bid_step', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('buyout_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('estimate_price_start', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('estimate_price_end', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('auction', ['Lot'])

        # Changing field 'Bid.lot'
        db.alter_column('auction_bid', 'lot_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auction.Lot']))


    def backwards(self, orm):

        # Adding model 'LotBase'
        db.create_table('auction_lotbase', (
            ('estimate_price_end', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start_price', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('bid_step', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('is_open', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('close_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('buyout_price', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('estimate_price_start', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('auction', ['LotBase'])

        # Deleting model 'Lot'
        db.delete_table('auction_lot')

        # Changing field 'Bid.lot'
        db.alter_column('auction_bid', 'lot_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auction.LotBase']))


    models = {
        'auction.bid': {
            'Meta': {'object_name': 'Bid'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_buyout': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auction.Lot']"}),
            'price': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'submit_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auction.lot': {
            'Meta': {'object_name': 'Lot'},
            'bid_step': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'buyout_price': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'close_date': ('django.db.models.fields.DateTimeField', [], {}),
            'estimate_price_end': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'estimate_price_start': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_open': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'start_price': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['auction']
