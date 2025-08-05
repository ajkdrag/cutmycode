from django import template
from django.utils.safestring import mark_safe
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name

register = template.Library()


@register.filter(name="syntax_highlight", needs_autoescape=True)
def syntax_highlight(value, language="python", autoescape=True):
    try:
        lexer = get_lexer_by_name(language)
        formatter = HtmlFormatter(wrapcode=True, style="one-dark")
        result = highlight(value, lexer, formatter)
        return mark_safe(result)
    except Exception:
        return value
