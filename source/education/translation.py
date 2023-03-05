from modeltranslation.translator import register, TranslationOptions
from education.models import Subject, Packet, Discount


@register(Subject)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Packet)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Discount)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)
