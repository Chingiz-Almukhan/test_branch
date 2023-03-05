from modeltranslation.translator import register, TranslationOptions
from applications.models import Status


@register(Status)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',)
