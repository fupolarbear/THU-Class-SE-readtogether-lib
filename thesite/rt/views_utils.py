import json

from django.http import HttpResponse, Http404


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


def POST_required(*field_list):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                return render_JSON_Error('Only POST method is accepted.')
            for field in field_list:
                if field not in request.POST:
                    return render_JSON_Error('POST data not found:{}.'.format(
                        field,
                        ))
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def login_required_JSON(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render_JSON_Error('Not logged in.')
        return func(request, *args, **kwargs)
    return wrapper


def catch_404_JSON(func):
    def wrapper(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Http404 as err:
            return render_JSON_Error('404 raised.', {
                'message': err.message,
                })
    return wrapper
