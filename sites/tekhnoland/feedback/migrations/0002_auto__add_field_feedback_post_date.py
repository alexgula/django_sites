# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Feedback.post_date'
        db.add_column('feedback_feedback', 'post_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2011, 6, 27, 1, 19, 44, 634000), blank=True), keep_default=False)

    def backwards(self, orm):

        # Deleting field 'Feedback.post_date'
        db.delete_column('feedback_feedback', 'post_date')

    models = {
        'feedback.feedback': {
            'Meta': {'object_name': 'Feedback'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'post_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['feedback']
