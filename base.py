#-*- coding : utf-8 -*-
import copy
from django.utils import six
from functools import update_wrapper
from django.utils import six

class BaseView(object):
    
    request = None
    kwargs = None
    args = None
    
    def __call__(self, request, *args, **kwargs):
        
        """
        as_view() like of django_master
        Main entry point for all views, we check some security about given arguments
        
        creating a deepcopy of the view to erase border effects
        updating the wrapper
        dispach to appropriate method, most of the time: get, post, delete
        
        """
        self = copy.deepcopy(self)
        self.request = request
        self.kwargs = kwargs
        self.args = args
        
        for key, value in six.iteritems(self.kwargs):
            if key not in self.__class__.http_method_names or self._dic_.keys():
                setattr(self, key, value)

        update_wrapper(self, self.__class__, updated=())
        update_wrapper(self, self.__call__ , assigned=())
            
        if self.request.method.lower() in self.__class__.http_method_names:
            dispach_method = getattr(self, self.request.method.lower())
            dispach_method()
        else:
            method = [m.upper() for m in self.__class__.http_method_names if hasattr(self, m)]
            return http.HttpResponseNotAllowed(method)
            
    def __str__(self):
        return self.__class__.__name__

class ModelBaseView(BaseView):
    """
    It's always fun to have a ModelBaseView
        
    """
    model = None
    context = None
