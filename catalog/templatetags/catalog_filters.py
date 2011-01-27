from django import template
from catalog.models import HeadphonesCategory

register = template.Library()

@register.inclusion_tag("tags/sidebar.html")
def category_list(request_path):
    active_categories = HeadphonesCategory.objects.filter(is_active=True)
    return {
        'active_categories': active_categories,
        'request_path': request_path
}
