# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Clinical'
        db.create_table('econmet_clinical', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('history_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('valid_to_study', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('econmet', ['Clinical'])

        # Adding M2M table for field illness on 'Clinical'
        db.create_table('econmet_clinical_illness', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinical', models.ForeignKey(orm['econmet.clinical'], null=False)),
            ('illness', models.ForeignKey(orm['econmet.illness'], null=False))
        ))
        db.create_unique('econmet_clinical_illness', ['clinical_id', 'illness_id'])

        # Adding M2M table for field analisys on 'Clinical'
        db.create_table('econmet_clinical_analisys', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinical', models.ForeignKey(orm['econmet.clinical'], null=False)),
            ('analisys', models.ForeignKey(orm['econmet.analisys'], null=False))
        ))
        db.create_unique('econmet_clinical_analisys', ['clinical_id', 'analisys_id'])

        # Adding M2M table for field symptoms on 'Clinical'
        db.create_table('econmet_clinical_symptoms', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinical', models.ForeignKey(orm['econmet.clinical'], null=False)),
            ('symptoms', models.ForeignKey(orm['econmet.symptoms'], null=False))
        ))
        db.create_unique('econmet_clinical_symptoms', ['clinical_id', 'symptoms_id'])

        # Adding M2M table for field report on 'Clinical'
        db.create_table('econmet_clinical_report', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('clinical', models.ForeignKey(orm['econmet.clinical'], null=False)),
            ('report', models.ForeignKey(orm['econmet.report'], null=False))
        ))
        db.create_unique('econmet_clinical_report', ['clinical_id', 'report_id'])

        # Adding model 'IllnessTranslation'
        db.create_table('econmet_illnesstranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.Illness'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('econmet', ['IllnessTranslation'])

        # Adding model 'Illness'
        db.create_table('econmet_illness', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rate_percent', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('econmet', ['Illness'])

        # Adding model 'Analisys'
        db.create_table('econmet_analisys', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('econmet', ['Analisys'])

        # Adding M2M table for field parameter_result on 'Analisys'
        db.create_table('econmet_analisys_parameter_result', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analisys', models.ForeignKey(orm['econmet.analisys'], null=False)),
            ('analisysparameterresult', models.ForeignKey(orm['econmet.analisysparameterresult'], null=False))
        ))
        db.create_unique('econmet_analisys_parameter_result', ['analisys_id', 'analisysparameterresult_id'])

        # Adding model 'AnalisysParameterResult'
        db.create_table('econmet_analisysparameterresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.AnalisysParameter'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.ParameterValues'])),
        ))
        db.send_create_signal('econmet', ['AnalisysParameterResult'])

        # Adding model 'AnalisysParameterTranslation'
        db.create_table('econmet_analisysparametertranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.AnalisysParameter'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('econmet', ['AnalisysParameterTranslation'])

        # Adding model 'AnalisysParameter'
        db.create_table('econmet_analisysparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_basic', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('econmet', ['AnalisysParameter'])

        # Adding M2M table for field parameter_values on 'AnalisysParameter'
        db.create_table('econmet_analisysparameter_parameter_values', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('analisysparameter', models.ForeignKey(orm['econmet.analisysparameter'], null=False)),
            ('parametervalues', models.ForeignKey(orm['econmet.parametervalues'], null=False))
        ))
        db.create_unique('econmet_analisysparameter_parameter_values', ['analisysparameter_id', 'parametervalues_id'])

        # Adding model 'ParameterValuesTranslation'
        db.create_table('econmet_parametervaluestranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.ParameterValues'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('econmet', ['ParameterValuesTranslation'])

        # Adding model 'ParameterValues'
        db.create_table('econmet_parametervalues', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('econmet', ['ParameterValues'])

        # Adding model 'Symptoms'
        db.create_table('econmet_symptoms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('econmet', ['Symptoms'])

        # Adding M2M table for field parameter_result on 'Symptoms'
        db.create_table('econmet_symptoms_parameter_result', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('symptoms', models.ForeignKey(orm['econmet.symptoms'], null=False)),
            ('symptomsparameterresult', models.ForeignKey(orm['econmet.symptomsparameterresult'], null=False))
        ))
        db.create_unique('econmet_symptoms_parameter_result', ['symptoms_id', 'symptomsparameterresult_id'])

        # Adding model 'SymptomsParameterResult'
        db.create_table('econmet_symptomsparameterresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parameter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.SymptomsParameter'])),
            ('value', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.ParameterValues'])),
        ))
        db.send_create_signal('econmet', ['SymptomsParameterResult'])

        # Adding model 'SymptomsParameterTranslate'
        db.create_table('econmet_symptomsparametertranslate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.SymptomsParameter'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('econmet', ['SymptomsParameterTranslate'])

        # Adding model 'SymptomsParameter'
        db.create_table('econmet_symptomsparameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('econmet', ['SymptomsParameter'])

        # Adding M2M table for field parameter_values on 'SymptomsParameter'
        db.create_table('econmet_symptomsparameter_parameter_values', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('symptomsparameter', models.ForeignKey(orm['econmet.symptomsparameter'], null=False)),
            ('parametervalues', models.ForeignKey(orm['econmet.parametervalues'], null=False))
        ))
        db.create_unique('econmet_symptomsparameter_parameter_values', ['symptomsparameter_id', 'parametervalues_id'])

        # Adding model 'Report'
        db.create_table('econmet_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('econmet', ['Report'])

        # Adding M2M table for field illness on 'Report'
        db.create_table('econmet_report_illness', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm['econmet.report'], null=False)),
            ('illness', models.ForeignKey(orm['econmet.illness'], null=False))
        ))
        db.create_unique('econmet_report_illness', ['report_id', 'illness_id'])

        # Adding M2M table for field parameters on 'Report'
        db.create_table('econmet_report_parameters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('report', models.ForeignKey(orm['econmet.report'], null=False)),
            ('analisysparameter', models.ForeignKey(orm['econmet.analisysparameter'], null=False))
        ))
        db.create_unique('econmet_report_parameters', ['report_id', 'analisysparameter_id'])

        # Adding model 'MedicalProfile'
        db.create_table('econmet_medicalprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('laboratory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['econmet.LaboratoryProfile'])),
        ))
        db.send_create_signal('econmet', ['MedicalProfile'])

        # Adding M2M table for field clinical on 'MedicalProfile'
        db.create_table('econmet_medicalprofile_clinical', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('medicalprofile', models.ForeignKey(orm['econmet.medicalprofile'], null=False)),
            ('clinical', models.ForeignKey(orm['econmet.clinical'], null=False))
        ))
        db.create_unique('econmet_medicalprofile_clinical', ['medicalprofile_id', 'clinical_id'])

        # Adding model 'LaboratoryProfile'
        db.create_table('econmet_laboratoryprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('econmet', ['LaboratoryProfile'])

    def backwards(self, orm):
        # Deleting model 'Clinical'
        db.delete_table('econmet_clinical')

        # Removing M2M table for field illness on 'Clinical'
        db.delete_table('econmet_clinical_illness')

        # Removing M2M table for field analisys on 'Clinical'
        db.delete_table('econmet_clinical_analisys')

        # Removing M2M table for field symptoms on 'Clinical'
        db.delete_table('econmet_clinical_symptoms')

        # Removing M2M table for field report on 'Clinical'
        db.delete_table('econmet_clinical_report')

        # Deleting model 'IllnessTranslation'
        db.delete_table('econmet_illnesstranslation')

        # Deleting model 'Illness'
        db.delete_table('econmet_illness')

        # Deleting model 'Analisys'
        db.delete_table('econmet_analisys')

        # Removing M2M table for field parameter_result on 'Analisys'
        db.delete_table('econmet_analisys_parameter_result')

        # Deleting model 'AnalisysParameterResult'
        db.delete_table('econmet_analisysparameterresult')

        # Deleting model 'AnalisysParameterTranslation'
        db.delete_table('econmet_analisysparametertranslation')

        # Deleting model 'AnalisysParameter'
        db.delete_table('econmet_analisysparameter')

        # Removing M2M table for field parameter_values on 'AnalisysParameter'
        db.delete_table('econmet_analisysparameter_parameter_values')

        # Deleting model 'ParameterValuesTranslation'
        db.delete_table('econmet_parametervaluestranslation')

        # Deleting model 'ParameterValues'
        db.delete_table('econmet_parametervalues')

        # Deleting model 'Symptoms'
        db.delete_table('econmet_symptoms')

        # Removing M2M table for field parameter_result on 'Symptoms'
        db.delete_table('econmet_symptoms_parameter_result')

        # Deleting model 'SymptomsParameterResult'
        db.delete_table('econmet_symptomsparameterresult')

        # Deleting model 'SymptomsParameterTranslate'
        db.delete_table('econmet_symptomsparametertranslate')

        # Deleting model 'SymptomsParameter'
        db.delete_table('econmet_symptomsparameter')

        # Removing M2M table for field parameter_values on 'SymptomsParameter'
        db.delete_table('econmet_symptomsparameter_parameter_values')

        # Deleting model 'Report'
        db.delete_table('econmet_report')

        # Removing M2M table for field illness on 'Report'
        db.delete_table('econmet_report_illness')

        # Removing M2M table for field parameters on 'Report'
        db.delete_table('econmet_report_parameters')

        # Deleting model 'MedicalProfile'
        db.delete_table('econmet_medicalprofile')

        # Removing M2M table for field clinical on 'MedicalProfile'
        db.delete_table('econmet_medicalprofile_clinical')

        # Deleting model 'LaboratoryProfile'
        db.delete_table('econmet_laboratoryprofile')

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