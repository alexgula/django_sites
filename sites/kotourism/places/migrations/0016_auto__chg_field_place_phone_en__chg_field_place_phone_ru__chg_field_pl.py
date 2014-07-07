# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Place.phone_en'
        db.alter_column('places_place', 'phone_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Place.phone_ru'
        db.alter_column('places_place', 'phone_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Place.timetable'
        db.alter_column('places_place', 'timetable', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Place.phone'
        db.alter_column('places_place', 'phone', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Place.timetable_uk'
        db.alter_column('places_place', 'timetable_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Place.timetable_en'
        db.alter_column('places_place', 'timetable_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Place.phone_uk'
        db.alter_column('places_place', 'phone_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))

        # Changing field 'Place.timetable_ru'
        db.alter_column('places_place', 'timetable_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True))


    def backwards(self, orm):

        # Changing field 'Place.phone_en'
        db.alter_column('places_place', 'phone_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Place.phone_ru'
        db.alter_column('places_place', 'phone_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Place.timetable'
        db.alter_column('places_place', 'timetable', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Place.phone'
        db.alter_column('places_place', 'phone', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Place.timetable_uk'
        db.alter_column('places_place', 'timetable_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Place.timetable_en'
        db.alter_column('places_place', 'timetable_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Place.phone_uk'
        db.alter_column('places_place', 'phone_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'Place.timetable_ru'
        db.alter_column('places_place', 'timetable_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))


    models = {
        'places.imagecontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'ImageContent', 'db_table': "'places_region_imagecontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagecontent_set'", 'to': "orm['places.Region']"}),
            'position': ('django.db.models.fields.CharField', [], {'default': "'left'", 'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'places.place': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['type', 'slug'],)", 'object_name': 'Place'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'address_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'address_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'interop_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'blank': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['places.Place']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'phone_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'phone_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'phone_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'timetable': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'timetable_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'timetable_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'timetable_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['places.PlaceType']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'places.placetype': {
            'Meta': {'object_name': 'PlaceType'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'code': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['places.PlaceType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'places.region': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['type', 'slug'],)", 'object_name': 'Region'},
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'template_key': ('django.db.models.fields.CharField', [], {'default': "'standart'", 'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'places.restructuredcontent': {
            'Meta': {'ordering': "['ordering']", 'object_name': 'RestructuredContent', 'db_table': "'places_region_restructuredcontent'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'restructuredcontent_set'", 'to': "orm['places.Region']"}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'text_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'text_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['places']
