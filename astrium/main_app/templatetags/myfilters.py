from django import template
import math

register = template.Library()

@register.filter
def get(mapping, key):
    return mapping.get(key, '')

@register.filter
def multiply(value, arg):
    return value * arg


@register.filter # (name='textNum', is_safe=False)
def textNum(val, precision=2):
    # print ("val", type(val))
    try:
        float_val = int(val)
    except ValueError:
        try:
            float_val = float(val)
            # float_val = math.floor(float_val)
        except:
            raise template.TemplateSyntaxError(
                f'Value must be an integer. {val} is not an integer')
    if float_val < 1000:
        return str(float_val)
    elif float_val > 1_000_000_000:
        return f'{float_val/1_000_000_000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'B'
    elif float_val < 1_000_000:
        return f'{ float_val/1000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'K'
    else:
        return f'{float_val/1_000_000.0:.{precision}f}'.rstrip('0').rstrip('.') + 'M'