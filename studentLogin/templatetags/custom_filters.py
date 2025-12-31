from django import template

register = template.Library()

@register.filter(name='add_class_and_placeholder')
def add_class_and_placeholder(field, args):
    css_class, placeholder = args.split(',')
    return field.as_widget(attrs={"class": css_class.strip(), "placeholder": placeholder.strip()})
