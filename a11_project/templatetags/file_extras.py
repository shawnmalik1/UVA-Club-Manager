from django import template

register = template.Library()

@register.filter
def is_image(file_url):
    return file_url.lower().endswith(('.jpg', '.jpeg', '.png'))

@register.filter
def is_text(file_url):
    return file_url.lower().endswith('.txt')