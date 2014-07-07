# coding=utf-8
from modeltranslation.translator import translator, TranslationOptions
from .catalogue.models import Category, Term, Author, ContemporaryType, LifePeriod, Owner, Work, Deal


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', )

translator.register(Category, CategoryTranslationOptions)


class TermTranslationOptions(TranslationOptions):
    fields = ('name', 'abbr', )

translator.register(Term, TermTranslationOptions)


class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', )

translator.register(Author, AuthorTranslationOptions)


class ContemporaryTypeTranslationOptions(TranslationOptions):
    fields = ('name', )

translator.register(ContemporaryType, ContemporaryTypeTranslationOptions)


class LifePeriodTranslationOptions(TranslationOptions):
    fields = ('name', 'bio', )

translator.register(LifePeriod, LifePeriodTranslationOptions)


class OwnerTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', )

translator.register(Owner, OwnerTranslationOptions)


class WorkTranslationOptions(TranslationOptions):
    fields = ('name', 'desc', )

translator.register(Work, WorkTranslationOptions)


class DealTranslationOptions(TranslationOptions):
    fields = ('desc', )

translator.register(Deal, DealTranslationOptions)
