import base64

from django.contrib.auth import authenticate, login
from django.http import HttpResponse

from ddns.models import Record


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
    from pprint import pformat
    if 'ipv4' not in request.GET and 'ipv6' not in request.GET:
        return HttpResponse("Must specify one or both of ipv4/ipv6 address\nParams:%s" % pformat(request.GET.dict()), status=400)
    if not u'domain' in request.GET:
        return HttpResponse("Must specify domain\nParams:%s" % pformat(request.GET.dict()), status=400)

    for ipvx, record_type in ((u'ipv4', 'A'), (u'ipv6', 'AAAA')):
        if ipvx not in request.GET:
            continue
        record, created = Record.objects.get_or_create(
            name=request.GET['domain'],
            type=record_type,
        )
        record.domain_id = 1
        record.ttl = 1
        record.auth = True
        record.content = request.GET[ipvx]
        record.save()

    return HttpResponse("Saved record(s)")
