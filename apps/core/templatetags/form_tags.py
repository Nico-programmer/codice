from django import forms, template

register = template.Library()


@register.filter
def styled(field):
    """Pinta el campo de un formulario con las clases del diseño (input, select, textarea).

    Así los formularios no tienen que repetir attrs={'class': 'input'} en cada widget.
    """
    widget = field.field.widget
    if isinstance(widget, forms.CheckboxInput):
        css = ''
    elif isinstance(widget, forms.Select):
        css = 'select'
    elif isinstance(widget, forms.Textarea):
        css = 'textarea'
    else:
        css = 'input'
    attrs = {'class': css} if css else {}
    if field.errors:
        attrs['aria-invalid'] = 'true'
        attrs['aria-describedby'] = f'{field.id_for_label}-error'
    return field.as_widget(attrs=attrs)
