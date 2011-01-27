from django import template
from catalog.models import Sections

register = template.Library()

@register.inclusion_tag("tags/sidebar.html")
def category_list(request_path):
    active_sections = Sections.objects.all()
    return {
        'request_path': request_path,
        'sections': active_sections
}
