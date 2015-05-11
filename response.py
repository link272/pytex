#-*- coding : utf-8 -*-
from base import BaseView
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse_lazy
from django import http

class ResponseBase(BaseView):
    
    """
        Response part of a view
        
    """
    
    template_name = None
    url_pattern = None
    
    def template(self):
        """
        Ending function, render a template
        
        """
        return TemplateResponse(request = self.request,
                                template = self.template_name,
                                context = self.context,
                                using = None)
                                
    def redirection(self):
        """
        Ending function, redirecting
        
        """
        url = reverse_lazy(self.url_pattern)
        return http.HttpResponseRedirect(url)
    
