# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'FamilyMember'
        db.create_table('family_familymember', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('birth_date', self.gf('django.db.models.fields.DateField')()),
            ('died_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('father_name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('preview', self.gf('django.db.models.fields.TextField')()),
            ('citation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('autor_of_citation', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('main_portrait', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title_for_main_portrait', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('family', ['FamilyMember'])

        # Adding model 'Picture'
        db.create_table('family_picture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['family.FamilyMember'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('family', ['Picture'])

    def backwards(self, orm):

        # Deleting model 'FamilyMember'
        db.delete_table('family_familymember')

        # Deleting model 'Picture'
        db.delete_table('family_picture')

    models = {
        'family.familymember': {
            'Meta': {'ordering': "('-surname',)", 'object_name': 'FamilyMember'},
            'autor_of_citation': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'birth_date': ('django.db.models.fields.DateField', [], {}),
            'citation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'died_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'father_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_portrait': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'preview': ('django.db.models.fields.TextField', [], {}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title_for_main_portrait': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'family.picture': {
            'Meta': {'ordering': "('-title',)", 'object_name': 'Picture'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['family.FamilyMember']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['family']
