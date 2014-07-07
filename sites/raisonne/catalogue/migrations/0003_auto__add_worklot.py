# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'WorkLot'
        db.create_table('catalogue_worklot', (
            ('lot_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auction.Lot'], unique=True, primary_key=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Work'])),
        ))
        db.send_create_signal('catalogue', ['WorkLot'])


    def backwards(self, orm):

        # Deleting model 'WorkLot'
        db.delete_table('catalogue_worklot')


    models = {
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
        'catalogue.author': {
            'Meta': {'object_name': 'Author', '_ormbases': ['catalogue.FacetModel']},
            'contemporaries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Author']", 'symmetrical': 'False', 'through': "orm['catalogue.AuthorContemporary']", 'blank': 'True'}),
            'date_birth': ('django.db.models.fields.DateField', [], {}),
            'date_death': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'desc_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_fr': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'facetmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.FacetModel']", 'unique': 'True', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'portrait': ('raisonne.mediatools.models.ImageFieldManaged', [], {'max_length': '100'}),
            'sign': ('raisonne.mediatools.models.ImageFieldManaged', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'catalogue.authorcontemporary': {
            'Meta': {'object_name': 'AuthorContemporary'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'linked'", 'to': "orm['catalogue.Author']"}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'person'", 'to': "orm['catalogue.Author']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.ContemporaryType']"}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'catalogue.category': {
            'Meta': {'ordering': "['weight', 'name']", 'object_name': 'Category'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.contemporarytype': {
            'Meta': {'object_name': 'ContemporaryType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.deal': {
            'Meta': {'object_name': 'Deal'},
            'buyer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'buyer'", 'null': 'True', 'to': "orm['catalogue.Owner']"}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seller': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seller'", 'null': 'True', 'to': "orm['catalogue.Owner']"}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Work']"})
        },
        'catalogue.facetmodel': {
            'Meta': {'object_name': 'FacetModel'},
            'filter': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'terms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.Term']", 'symmetrical': 'False'})
        },
        'catalogue.lifeperiod': {
            'Meta': {'object_name': 'LifePeriod'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Author']"}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'bio_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'year_begin': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'year_end': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.owner': {
            'Meta': {'object_name': 'Owner'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'desc_en': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_fr': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.term': {
            'Meta': {'ordering': "['weight', 'name']", 'object_name': 'Term'},
            'abbr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'abbr_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'abbr_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'abbr_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'abbr_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'weight': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'catalogue.work': {
            'Meta': {'unique_together': "(('author', 'slug'),)", 'object_name': 'Work', '_ormbases': ['catalogue.FacetModel']},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Author']"}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_fr': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'facetmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['catalogue.FacetModel']", 'unique': 'True', 'primary_key': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image': ('raisonne.mediatools.models.ImageFieldManaged', [], {'max_length': '100', 'blank': 'True'}),
            'image_offset_h': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'image_offset_v': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_fr': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Owner']", 'null': 'True', 'blank': 'True'}),
            'periods': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['catalogue.LifePeriod']", 'symmetrical': 'False', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rating_score': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'rating_value': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'width': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'years': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'catalogue.worklot': {
            'Meta': {'object_name': 'WorkLot', '_ormbases': ['auction.Lot']},
            'lot_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auction.Lot']", 'unique': 'True', 'primary_key': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['catalogue.Work']"})
        }
    }

    complete_apps = ['catalogue']
