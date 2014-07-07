# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Slide'
        db.create_table(u'slideshow_slide', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=250)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('gotolink', self.gf('django.db.models.fields.URLField')(max_length=250, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'slideshow', ['Slide'])


    def backwards(self, orm):
        # Deleting model 'Slide'
        db.delete_table(u'slideshow_slide')


    models = {
        u'slideshow.slide': {
            'Meta': {'object_name': 'Slide'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'gotolink': ('django.db.models.fields.URLField', [], {'max_length': '250', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '250'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        }
    }

    complete_apps = ['slideshow']