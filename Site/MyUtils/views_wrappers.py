from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import Http404, redirect


def log_execution_time(foo: callable):
    def wrapper(*args, **kwargs):
        st = time()
        resp = foo(*args, **kwargs)
        et = time() - st

        print(f'---# Foo "pr" finished in {et}s #---')

        return resp
    return wrapper


def login_required(foo: callable):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_authenticated:
            return redirect('login')

        resp = foo(*args, **kwargs)
        return resp

    return wrapper


def log_session(foo: callable):
    def wrapper(*args, **kwargs):
        request = args[0]
        results = list([f'{key}: {request.session[key]}'] for key in request.session.keys())
        print(results)
        resp = foo(*args, **kwargs)
        return resp

    return wrapper
