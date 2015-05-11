#-*- coding : utf-8 -*-
import logging
from form import FormBase
from display import DisplayBase
from response import ResponseBase
from delete import DeleteBase

class QuickView(FormBase, DisplayBase, Responsebase, DeleteBase):
    
    """
        You need to build your own view from this one, basically, just write get() and post() fonctions:
        
        For simple views:
        In any case you need to pass model, suffix arguments
                            set attributes                   get()                       post()
        ListView      | --                     | listing()  + template()   | --                          |
        PaginatedView | --                     | paginate() + template()   | --                          |
        DetailView    | --                     | detail()   + template()   | --                          |
        CreateView    | fields + url_pattern   | form()     + template()   | saveform()  + redirection() |
        UpdateView    | fields + url_pattern   | Uform()    + template()   | saveUform() + redirection() |
        DeleteView    | url_pattern            | detail()   + template()   | remove()    + redirection() |
        
        class Exemple1ListView(QuickView):
        
            model = Object1
            suffix = "list"
        
            def get():
                self.listing()
                self.template()
                
        url(r'^$', login_required(Exemple1ListView()), name = "objects1_list")
        
        OR:
        
        class Exemple2ListView(QuickView):
        
            def get():
                self.listing()
                self.template()
                
        url(r'^$', login_required(Exemple1ListView(Object1, "list")), name = "objects1_list")
        
        OR:
        
        class Exemple3CreateView(QuickView):
        
            url_pattern = "object1_list"
        
            def get():
                self.form
                self.template()
                
            def post():
                self.saveform()
                self.redirect()
            
                
        url(r'^$', login_required(Exemple3CreateView(Object1, "form")), name = "objects1_form")
        
        
        
        For to combine multiples objects:
        
        class Exemple4View(QuickView):
            
            url_pattern = "object_list"
            template_name = "object_app/exemple.html"
            
            def get():
                self.listing()
                self.model = Objects2
                self.detail(pk_pattern)
                self.model = Objects3
                self.form()
                self.context.update({"today_date": time.strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()))
                self.template()
            
            def post()
                self.model = Objects3
                self.saveform()
                self.redirection()
        
        """
    
    http_method_names = ['get', 
                        'post', 
                        'put', 
                        'patch', 
                        'delete', 
                        'head', 
                        'options', 
                        'trace']
        
        
    def __init__(self, model = None, suffix = None):
        
        """
        Initialisation of a view, if "model" is provided, it will be use in several fonction:
        (listing, paginate, form, saveform, Uform, saveUform, delete)
        
        if template_name attribute is not set, template_name = "object_app/object_name" is generated
        you can add any suffix you want to it, commons ones are detailed in the doc of each functions
        """
        
        self.suffix = suffix
        if model != None:
            self.model = model
            self.model_name = model._meta.model_name
            self.model_app = model._meta.model_app
            if self.template_name == None:
                self.template_name = "%s/%s" % (self.model_app, self.model_name)
                if self.suffix != None:
                    self.template_name += "_" + suffix + ".html"
        self.logger = logging.getLogger('django.request')
        self.context = dict()
