# coding=utf-8
from copy import copy
from modeltranslation.settings import DEFAULT_LANGUAGE
from modeltranslation.translator import translator
from feincms.admin.item_editor import FeinCMSInline


class TranslationAdminBase(object):
    """
    Mixin class which adds patch_translation_field functionality.

    Copied the class instead of just using due to import bug on production.
    """
    orig_was_required = {}

    def patch_translation_field(self, db_field, field, **kwargs):
        trans_opts = translator.get_options_for_model(self.model)

        # Hide the original field by making it non-editable.
        if db_field.name in trans_opts.fields:
            db_field.editable = False

            if field.required:
                field.required = False
                field.blank = True
                self.orig_was_required[\
                '%s.%s' % (db_field.model._meta, db_field.name)] = True

        # For every localized field copy the widget from the original field
        # and add a css class to identify a modeltranslation widget.
        if db_field.name in trans_opts.localized_fieldnames_rev:
            orig_fieldname = trans_opts.localized_fieldnames_rev[db_field.name]
            orig_formfield = self.formfield_for_dbfield(\
                self.model._meta.get_field(orig_fieldname),
                **kwargs)
            field.widget = copy(orig_formfield.widget)
            css_classes = field.widget.attrs.get('class', '').split(' ')
            css_classes.append('modeltranslation')

            if db_field.language == DEFAULT_LANGUAGE:
                # Add another css class to identify a default modeltranslation
                # widget.
                css_classes.append('modeltranslation-default')
                if orig_formfield.required or\
                   self.orig_was_required.get('%s.%s' % (db_field.model._meta,
                                                         orig_fieldname)):
                    # In case the original form field was required, make the
                    # default translation field required instead.
                    orig_formfield.required = False
                    orig_formfield.blank = True
                    field.required = True
                    field.blank = False

            field.widget.attrs['class'] = ' '.join(css_classes)


class TranslatedFeinCMSInline(FeinCMSInline, TranslationAdminBase):

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Call the baseclass function to get the formfield
        field = super(TranslatedFeinCMSInline, self).formfield_for_dbfield(db_field, **kwargs)
        self.patch_translation_field(db_field, field, **kwargs)
        return field
