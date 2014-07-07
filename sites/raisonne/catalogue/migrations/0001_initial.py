# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Category'
        db.create_table('catalogue_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Category'])

        # Adding model 'Term'
        db.create_table('catalogue_term', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Category'])),
            ('abbr', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('abbr_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('abbr_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('abbr_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('abbr_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Term'])

        # Adding model 'FacetModel'
        db.create_table('catalogue_facetmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filter', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('catalogue', ['FacetModel'])

        # Adding M2M table for field terms on 'FacetModel'
        db.create_table('catalogue_facetmodel_terms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facetmodel', models.ForeignKey(orm['catalogue.facetmodel'], null=False)),
            ('term', models.ForeignKey(orm['catalogue.term'], null=False))
        ))
        db.create_unique('catalogue_facetmodel_terms', ['facetmodel_id', 'term_id'])

        # Adding model 'Author'
        db.create_table('catalogue_author', (
            ('facetmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.FacetModel'], unique=True, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('desc_uk', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_fr', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('date_birth', self.gf('django.db.models.fields.DateField')()),
            ('date_death', self.gf('django.db.models.fields.DateField')()),
            ('portrait', self.gf('raisonne.mediatools.models.ImageFieldManaged')(max_length=100)),
            ('sign', self.gf('raisonne.mediatools.models.ImageFieldManaged')(max_length=100)),
        ))
        db.send_create_signal('catalogue', ['Author'])

        # Adding model 'ContemporaryType'
        db.create_table('catalogue_contemporarytype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['ContemporaryType'])

        # Adding model 'AuthorContemporary'
        db.create_table('catalogue_authorcontemporary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='person', to=orm['catalogue.Author'])),
            ('linked', self.gf('django.db.models.fields.related.ForeignKey')(related_name='linked', to=orm['catalogue.Author'])),
            ('weight', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.ContemporaryType'])),
        ))
        db.send_create_signal('catalogue', ['AuthorContemporary'])

        # Adding model 'LifePeriod'
        db.create_table('catalogue_lifeperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Author'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('year_begin', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('year_end', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('bio_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bio_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bio_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('bio_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['LifePeriod'])

        # Adding model 'Owner'
        db.create_table('catalogue_owner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('desc_fr', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Owner'])

        # Adding model 'Work'
        db.create_table('catalogue_work', (
            ('facetmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['catalogue.FacetModel'], unique=True, primary_key=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('rating_score', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('rating_value', self.gf('django.db.models.fields.FloatField')(default=1.0)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Author'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('name_uk', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('name_fr', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('years', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('width', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('image', self.gf('raisonne.mediatools.models.ImageFieldManaged')(max_length=100, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Owner'], null=True, blank=True)),
            ('image_offset_h', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image_offset_v', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('catalogue', ['Work'])

        # Adding unique constraint on 'Work', fields ['author', 'slug']
        db.create_unique('catalogue_work', ['author_id', 'slug'])

        # Adding M2M table for field periods on 'Work'
        db.create_table('catalogue_work_periods', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('work', models.ForeignKey(orm['catalogue.work'], null=False)),
            ('lifeperiod', models.ForeignKey(orm['catalogue.lifeperiod'], null=False))
        ))
        db.create_unique('catalogue_work_periods', ['work_id', 'lifeperiod_id'])

        # Adding model 'Deal'
        db.create_table('catalogue_deal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['catalogue.Work'])),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('seller', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='seller', null=True, to=orm['catalogue.Owner'])),
            ('buyer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='buyer', null=True, to=orm['catalogue.Owner'])),
            ('price', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('desc_uk', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_ru', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_en', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('desc_fr', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('catalogue', ['Deal'])


    def backwards(self, orm):

        # Removing unique constraint on 'Work', fields ['author', 'slug']
        db.delete_unique('catalogue_work', ['author_id', 'slug'])

        # Deleting model 'Category'
        db.delete_table('catalogue_category')

        # Deleting model 'Term'
        db.delete_table('catalogue_term')

        # Deleting model 'FacetModel'
        db.delete_table('catalogue_facetmodel')

        # Removing M2M table for field terms on 'FacetModel'
        db.delete_table('catalogue_facetmodel_terms')

        # Deleting model 'Author'
        db.delete_table('catalogue_author')

        # Deleting model 'ContemporaryType'
        db.delete_table('catalogue_contemporarytype')

        # Deleting model 'AuthorContemporary'
        db.delete_table('catalogue_authorcontemporary')

        # Deleting model 'LifePeriod'
        db.delete_table('catalogue_lifeperiod')

        # Deleting model 'Owner'
        db.delete_table('catalogue_owner')

        # Deleting model 'Work'
        db.delete_table('catalogue_work')

        # Removing M2M table for field periods on 'Work'
        db.delete_table('catalogue_work_periods')

        # Deleting model 'Deal'
        db.delete_table('catalogue_deal')


    models = {
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
        }
    }

    complete_apps = ['catalogue']
