from modeltranslation.translator import register, TranslationOptions
from .models import *
from django.utils.translation import gettext_lazy as _


@register(Salesman)
class SalesmanTranslationOptions(TranslationOptions):
    fields = ('full_name', 'city',)
    fallback_values = _('-- sorry, no translation provided --')


@register(Customer)
class CustomerTranslationOptions(TranslationOptions):
    fields = ('name', 'city',)
    fallback_values = _('-- sorry, no translation provided --')


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)
    fallback_values = _('-- sorry, no translation provided --')
