# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('cms_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('image_active', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('image_inactive', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('cms', ['Language'])

        # Adding model 'PageTranslation'
        db.create_table('cms_pagetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['PageTranslation'])

        # Adding model 'Page'
        db.create_table('cms_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('cms', ['Page'])

        # Adding model 'MenuTranslation'
        db.create_table('cms_menutranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Menu'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('cms', ['MenuTranslation'])

        # Adding model 'Menu'
        db.create_table('cms_menu', (
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('nav_option', self.gf('django.db.models.fields.CharField')(max_length=100, primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Page'])),
            ('show_owner_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('parent_menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Menu'], null=True, blank=True)),
        ))
        db.send_create_signal('cms', ['Menu'])

        # Adding model 'FixedValueTranslation'
        db.create_table('cms_fixedvaluetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.FixedValue'])),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cms', ['FixedValueTranslation'])

        # Adding model 'FixedValue'
        db.create_table('cms_fixedvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cms', ['FixedValue'])

        # Adding model 'Configuration'
        db.create_table('cms_configuration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('data_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('cms', ['Configuration'])

        # Adding model 'QuestionaryTranslation'
        db.create_table('cms_questionarytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Questionary'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['QuestionaryTranslation'])

        # Adding model 'Questionary'
        db.create_table('cms_questionary', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cms', ['Questionary'])

        # Adding M2M table for field questions on 'Questionary'
        db.create_table('cms_questionary_questions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionary', models.ForeignKey(orm['cms.questionary'], null=False)),
            ('question', models.ForeignKey(orm['cms.question'], null=False))
        ))
        db.create_unique('cms_questionary_questions', ['questionary_id', 'question_id'])

        # Adding M2M table for field parameters on 'Questionary'
        db.create_table('cms_questionary_parameters', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionary', models.ForeignKey(orm['cms.questionary'], null=False)),
            ('parameter', models.ForeignKey(orm['cms.parameter'], null=False))
        ))
        db.create_unique('cms_questionary_parameters', ['questionary_id', 'parameter_id'])

        # Adding model 'QuestionTranslation'
        db.create_table('cms_questiontranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Question'])),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['QuestionTranslation'])

        # Adding model 'Question'
        db.create_table('cms_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('response_text', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('just_one_response', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cms', ['Question'])

        # Adding M2M table for field complex_question on 'Question'
        db.create_table('cms_question_complex_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_question', models.ForeignKey(orm['cms.question'], null=False)),
            ('to_question', models.ForeignKey(orm['cms.question'], null=False))
        ))
        db.create_unique('cms_question_complex_question', ['from_question_id', 'to_question_id'])

        # Adding M2M table for field responses on 'Question'
        db.create_table('cms_question_responses', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['cms.question'], null=False)),
            ('response', models.ForeignKey(orm['cms.response'], null=False))
        ))
        db.create_unique('cms_question_responses', ['question_id', 'response_id'])

        # Adding model 'ParameterTranslation'
        db.create_table('cms_parametertranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Parameter'])),
            ('parameter', self.gf('django.db.models.fields.TextField')()),
            ('unit', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cms', ['ParameterTranslation'])

        # Adding model 'Parameter'
        db.create_table('cms_parameter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('is_required', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cms', ['Parameter'])

        # Adding model 'ResponseTranslation'
        db.create_table('cms_responsetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Language'])),
            ('model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cms.Response'])),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cms', ['ResponseTranslation'])

        # Adding model 'Response'
        db.create_table('cms_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('cms', ['Response'])

    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table('cms_language')

        # Deleting model 'PageTranslation'
        db.delete_table('cms_pagetranslation')

        # Deleting model 'Page'
        db.delete_table('cms_page')

        # Deleting model 'MenuTranslation'
        db.delete_table('cms_menutranslation')

        # Deleting model 'Menu'
        db.delete_table('cms_menu')

        # Deleting model 'FixedValueTranslation'
        db.delete_table('cms_fixedvaluetranslation')

        # Deleting model 'FixedValue'
        db.delete_table('cms_fixedvalue')

        # Deleting model 'Configuration'
        db.delete_table('cms_configuration')

        # Deleting model 'QuestionaryTranslation'
        db.delete_table('cms_questionarytranslation')

        # Deleting model 'Questionary'
        db.delete_table('cms_questionary')

        # Removing M2M table for field questions on 'Questionary'
        db.delete_table('cms_questionary_questions')

        # Removing M2M table for field parameters on 'Questionary'
        db.delete_table('cms_questionary_parameters')

        # Deleting model 'QuestionTranslation'
        db.delete_table('cms_questiontranslation')

        # Deleting model 'Question'
        db.delete_table('cms_question')

        # Removing M2M table for field complex_question on 'Question'
        db.delete_table('cms_question_complex_question')

        # Removing M2M table for field responses on 'Question'
        db.delete_table('cms_question_responses')

        # Deleting model 'ParameterTranslation'
        db.delete_table('cms_parametertranslation')

        # Deleting model 'Parameter'
        db.delete_table('cms_parameter')

        # Deleting model 'ResponseTranslation'
        db.delete_table('cms_responsetranslation')

        # Deleting model 'Response'
        db.delete_table('cms_response')

    models = {
        'cms.configuration': {
            'Meta': {'object_name': 'Configuration'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        'cms.fixedvalue': {
            'Meta': {'object_name': 'FixedValue'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cms.fixedvaluetranslation': {
            'Meta': {'object_name': 'FixedValueTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.FixedValue']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cms.language': {
            'Meta': {'object_name': 'Language'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_active': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'image_inactive': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'cms.menu': {
            'Meta': {'object_name': 'Menu'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'nav_option': ('django.db.models.fields.CharField', [], {'max_length': '100', 'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'parent_menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Menu']", 'null': 'True', 'blank': 'True'}),
            'show_owner_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cms.menutranslation': {
            'Meta': {'object_name': 'MenuTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'cms.page': {
            'Meta': {'object_name': 'Page'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'cms.pagetranslation': {
            'Meta': {'object_name': 'PageTranslation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Page']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'cms.parameter': {
            'Meta': {'object_name': 'Parameter'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'cms.parametertranslation': {
            'Meta': {'object_name': 'ParameterTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Parameter']"}),
            'parameter': ('django.db.models.fields.TextField', [], {}),
            'unit': ('django.db.models.fields.TextField', [], {})
        },
        'cms.question': {
            'Meta': {'object_name': 'Question'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'complex_question': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cms.Question']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'just_one_response': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'response_text': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responses': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cms.Response']", 'null': 'True', 'blank': 'True'})
        },
        'cms.questionary': {
            'Meta': {'object_name': 'Questionary'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parameters': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Parameter']", 'symmetrical': 'False'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cms.Question']", 'symmetrical': 'False'})
        },
        'cms.questionarytranslation': {
            'Meta': {'object_name': 'QuestionaryTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Questionary']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'cms.questiontranslation': {
            'Meta': {'object_name': 'QuestionTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Question']"}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'cms.response': {
            'Meta': {'object_name': 'Response'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'cms.responsetranslation': {
            'Meta': {'object_name': 'ResponseTranslation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Language']"}),
            'model': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cms.Response']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['cms']