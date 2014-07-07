# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Slide'
        db.create_table('slideshow_slide', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('slide', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('map_lon', self.gf('django.db.models.fields.FloatField')()),
            ('map_lat', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('slideshow', ['Slide'])


    def backwards(self, orm):

        # Deleting model 'Slide'
        db.delete_table('slideshow_slide')


    models = {
        'slideshow.slide': {
            'Meta': {'object_name': 'Slide'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'desc_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_ru': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'desc_uk': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'map_lat': ('django.db.models.fields.FloatField', [], {}),
            'map_lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'name_uk': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'slide': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'})
        }
    }

    complete_apps = ['slideshow']
