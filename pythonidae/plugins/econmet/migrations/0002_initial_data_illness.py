# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import DataMigration
from plugins.econmet.migracion_datos import process_data, delete_users


class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        process_data()

    def backwards(self, orm):
        "Write your backwards methods here."
        delete_users()

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
        'cms.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_active': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image_inactive': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'econmet.analisys': {
            'Meta': {'object_name': 'Analisys'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter_result': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['econmet.AnalisysParameterResult']", 'symmetrical': 'False'})
        },
        'econmet.analisysparameter': {
            'Meta': {'object_name': 'AnalisysParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_basic': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'parameter_values': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.ParameterValues']", 'null': 'True', 'blank': 'True'})
        },
        'econmet.analisysparameterresult': {
            'Meta': {'object_name': 'AnalisysParameterResult'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.AnalisysParameter']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.ParameterValues']"})
        },
        'econmet.analisysparametertranslation': {
            'Meta': {'object_name': 'AnalisysParameterTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.AnalisysParameter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'econmet.clinical': {
            'Meta': {'object_name': 'Clinical'},
            'analisys': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.Analisys']", 'null': 'True', 'blank': 'True'}),
            'history_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'illness': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.Illness']", 'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.Report']", 'null': 'True', 'blank': 'True'}),
            'symptoms': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.Symptoms']", 'null': 'True', 'blank': 'True'}),
            'valid_to_study': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'econmet.illness': {
            'Meta': {'object_name': 'Illness'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate_percent': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'econmet.illnesstranslation': {
            'Meta': {'object_name': 'IllnessTranslation'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.Illness']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'econmet.laboratoryprofile': {
            'Meta': {'object_name': 'LaboratoryProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'econmet.medicalprofile': {
            'Meta': {'object_name': 'MedicalProfile'},
            'clinical': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.Clinical']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'laboratory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.LaboratoryProfile']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'econmet.parametervalues': {
            'Meta': {'object_name': 'ParameterValues'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'econmet.parametervaluestranslation': {
            'Meta': {'object_name': 'ParameterValuesTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.ParameterValues']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'econmet.report': {
            'Meta': {'object_name': 'Report'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'illness': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['econmet.Illness']", 'symmetrical': 'False'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['econmet.AnalisysParameter']", 'symmetrical': 'False'})
        },
        'econmet.symptoms': {
            'Meta': {'object_name': 'Symptoms'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter_result': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['econmet.SymptomsParameterResult']", 'symmetrical': 'False'})
        },
        'econmet.symptomsparameter': {
            'Meta': {'object_name': 'SymptomsParameter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter_values': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['econmet.ParameterValues']", 'null': 'True', 'blank': 'True'})
        },
        'econmet.symptomsparameterresult': {
            'Meta': {'object_name': 'SymptomsParameterResult'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.SymptomsParameter']"}),
            'value': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.ParameterValues']"})
        },
        'econmet.symptomsparametertranslate': {
            'Meta': {'object_name': 'SymptomsParameterTranslate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['econmet.SymptomsParameter']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['econmet']