# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'PriceType'
        db.create_table('catalog_pricetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('currency_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('load_state', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['PriceType'])

        # Adding model 'Product'
        db.create_table('catalog_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('part_number', self.gf('django.db.models.fields.CharField')(max_length=25, blank=True)),
            ('part_number_search', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=25, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('load_state', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['Product'])

        # Adding M2M table for field replacements on 'Product'
        db.create_table('catalog_product_replacements', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_product', models.ForeignKey(orm['catalog.product'], null=False)),
            ('to_product', models.ForeignKey(orm['catalog.product'], null=False))
        ))
        db.create_unique('catalog_product_replacements', ['from_product_id', 'to_product_id'])

        # Adding model 'ProductStockUnit'
        db.create_table('catalog_productstockunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('pending', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('load_state', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalog', ['ProductStockUnit'])

        # Adding unique constraint on 'ProductStockUnit', fields ['product', 'stock']
        db.create_unique('catalog_productstockunit', ['product_id', 'stock'])

        # Adding model 'ProductStockUnitPrice'
        db.create_table('catalog_productstockunitprice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('price_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.PriceType'])),
            ('stock_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ProductStockUnit'])),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('multiplier', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
        ))
        db.send_create_signal('catalog', ['ProductStockUnitPrice'])

        # Adding model 'Order'
        db.create_table('catalog_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('payment_type', self.gf('django.db.models.fields.IntegerField')()),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('currency_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('sum', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('comment', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('catalog', ['Order'])

        # Adding model 'OrderItem'
        db.create_table('catalog_orderitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.Product'])),
            ('stock', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('pending', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('sum', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('multiplier', self.gf('django.db.models.fields.DecimalField')(max_digits=16, decimal_places=4)),
            ('is_replacement', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalog', ['OrderItem'])

        # Adding model 'BasketItem'
        db.create_table('catalog_basketitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock_unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalog.ProductStockUnit'])),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
            ('is_replacement', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('catalog', ['BasketItem'])

        # Adding unique constraint on 'BasketItem', fields ['stock_unit', 'customer']
        db.create_unique('catalog_basketitem', ['stock_unit_id', 'customer_id'])

    def backwards(self, orm):

        # Removing unique constraint on 'BasketItem', fields ['stock_unit', 'customer']
        db.delete_unique('catalog_basketitem', ['stock_unit_id', 'customer_id'])

        # Removing unique constraint on 'ProductStockUnit', fields ['product', 'stock']
        db.delete_unique('catalog_productstockunit', ['product_id', 'stock'])

        # Deleting model 'PriceType'
        db.delete_table('catalog_pricetype')

        # Deleting model 'Product'
        db.delete_table('catalog_product')

        # Removing M2M table for field replacements on 'Product'
        db.delete_table('catalog_product_replacements')

        # Deleting model 'ProductStockUnit'
        db.delete_table('catalog_productstockunit')

        # Deleting model 'ProductStockUnitPrice'
        db.delete_table('catalog_productstockunitprice')

        # Deleting model 'Order'
        db.delete_table('catalog_order')

        # Deleting model 'OrderItem'
        db.delete_table('catalog_orderitem')

        # Deleting model 'BasketItem'
        db.delete_table('catalog_basketitem')

    models = {
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
        'catalog.basketitem': {
            'Meta': {'unique_together': "(('stock_unit', 'customer'),)", 'object_name': 'BasketItem'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_replacement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'stock_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductStockUnit']"})
        },
        'catalog.order': {
            'Meta': {'object_name': 'Order'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_type': ('django.db.models.fields.IntegerField', [], {}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'sum': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'})
        },
        'catalog.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_replacement': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multiplier': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Order']"}),
            'pending': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sum': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'catalog.pricetype': {
            'Meta': {'ordering': "['name']", 'object_name': 'PriceType'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'currency_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'catalog.product': {
            'Meta': {'ordering': "['part_number']", 'object_name': 'Product'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'part_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'part_number_search': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'blank': 'True'}),
            'replacements': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalog.Product']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'catalog.productstockunit': {
            'Meta': {'unique_together': "(('product', 'stock'),)", 'object_name': 'ProductStockUnit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'load_state': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pending': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.Product']"}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'stock': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'catalog.productstockunitprice': {
            'Meta': {'object_name': 'ProductStockUnitPrice'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiplier': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '16', 'decimal_places': '4'}),
            'price_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.PriceType']"}),
            'stock_unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalog.ProductStockUnit']"}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['catalog']
