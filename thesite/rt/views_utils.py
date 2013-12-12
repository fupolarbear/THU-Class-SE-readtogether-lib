import json

from django.http import HttpResponse


def FC(prototype, *args):
    """Fake a object-like variable for templates based on the prototype."""
    return dict(zip(prototype, args))


def render_JSON_OK(data):
    """Shortcut. Render an OK message with data in JSON.
    
    Argument:
    data -- dict, data to be sent
    """
    data['status'] = 'OK'
    return HttpResponse(json.dumps(data))


def render_JSON_Error(message, data={}):
    """Shortcut. Render an Error message in JSON.
    
    Argument:
    message -- str, human-readable (but English) error message
    data    -- detailed error data to be sent
    """
    res = {
        'status': 'Error',
        'err': message,
        }
    res.update(data)
    return HttpResponse(json.dumps(res))
