from django.contrib.auth.models import User
from projects.models import Project
from builds.models import Version
from django.db import models
from django.core.urlresolvers import resolve
from django.shortcuts import get_object_or_404


class PageView(models.Model):
    """
    Stores things common to all requests we might want to track.
    """
    url = models.URLField()
    user = models.ForeignKey(User, null=True) #null user = anon
    timestamp = models.DateTimeField(auto_now=True)
    #todo: more fields?
    
    class Meta:
        abstract=True
        
    
class DocView(PageView):
    """
    Stores a hit on a documentation page, associating more tightly with 
    project/version/language/etc than a bare url.
    """
    project = models.ForeignKey(Project)
    version = models.ForeignKey(Version)
    language = models.CharField(max_length=2) #e.g.: en, sp, ge
    sphinx_filename = models.CharField(max_length=256) #probably excessive
    
    @staticmethod
    def from_url(url):
        """
        Helper method to generate a DocView object from a url.
        This looks a whole lot like the parsing of a request for docs_detail; 
        this is because it essentially dispatches the url provided to 
        get the view details.
        
        TODO: this probably could be abstracted into a fairly awesome-but-useless framework.
        """
        
        res = resolve(url)
        kwargs = res.kwargs
        proj = get_object_or_404(Project, slug=kwargs['project_slug'])
        if kwargs.get('version_slug'):
            version_slug = kwargs['version_slug']
        else:
            version_slug = proj.get_default_version()
        version = Version.objects.get(project=proj, slug=version_slug)
        language = kwargs.get('lang_slug', 'en')
        filename = kwargs.get('filename', 'index.html')
        return DocView(project=proj,
                       version=version,
                       url=url,
                       language=language,
                       sphinx_filename = filename
                       )
                                
        
        
        
