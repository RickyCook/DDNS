import base64

from django.contrib.auth import authenticate, login
from django.http import HttpResponse


def basic_http_auth(f):
    """
    Basic HTTP auth decorator
    http://learningdjango.blogspot.com.au/2012/04/basic-http-authentication-in-django.html
    """
    def wrap(request, *args, **kwargs):
        if request.META.get('HTTP_AUTHORIZATION', False):
            authtype, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
            auth = base64.b64decode(auth)
            username, password = auth.split(':')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return f(request, *args, **kwargs)
            else:
                r = HttpResponse("Auth Required", status = 401)
                r['WWW-Authenticate'] = 'Basic realm="ThatPanda DDNS"'
                return r
        r = HttpResponse("Auth Required", status = 401)
        r['WWW-Authenticate'] = 'Basic realm="ThatPanda DDNS"'
        return r
        
    return wrap


@basic_http_auth
def update(request):
    """
    Service an update request in the form of
    /update?ipv6=<ip6addr>&ipv4=<ipaddr>&domain=<domain>
    """
    import datetime
    return HttpResponse("<html><body>It is now %s.</body></html>" % datetime.datetime.now())
