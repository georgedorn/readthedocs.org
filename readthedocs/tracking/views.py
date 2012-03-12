from django.core.urlresolvers import resolve
from django.http import HttpResponse, HttpResponseRedirect, \
    HttpResponsePermanentRedirect, Http404, HttpResponseNotFound
from tracking.models import DocView

def log_page_view(request):
    """
    Intended to be used asynchronously, with an ajax callback
    with page details.  
    """
    url = request.GET.get('url')
    dispatched = resolve(url)
    
    if dispatched.url_name.startswith('docs') \
        or dispatched.view_name.startswith('docs'):
        
        dv = DocView.from_url(url)
        dv.user = request.user
        
    