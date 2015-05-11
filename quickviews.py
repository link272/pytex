#-*- coding : utf-8 -*-
import logging
import copy
from django.forms import models as model_forms
from django.template.response import TemplateResponse
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse_lazy
from django import http
from django.utils import six
from functools import update_wrapper

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

    
        
class FormBase(ModelBaseView):
    
    """
        Views based on form
        
    """
    fields = None
    
    def form(self):
        
        """
        
        create a Form to be sent back by client
                            
        Common suffix: "form"
        
        Template exemple:
        
{% extends "base.html" %}
{% block content %}
<form action="" method="post">{% csrf_token %}
    {{ object1_form.as_table }}
	{% if object1_detail.id %}
    <input type="submit" value="Update" />
	{% else %}
	<input type="submit" value="Create" />
	{% endif %}
</form>
  <a href="{% url "object1_list" %}">No, cancel.</a>
{% endblock %}
        """
        context_name = self.model_name + "_form"
        try:
            form = model_forms.modelform_factory(model = self.model, fields = self.fields)
        except:
            form = None
        self.context[context_name] = form
        
    def saveform(self):
        """
        
        extract objects from form and save it, return True if everything is ok.
        """
        try:
            form = model_forms.modelform_factory(model = self.model, fields = self.fields)
            form = form(**{'data': self.request.POST, 'files': self.request.FILES})
            
            if form.is_valid():
                objects = form.save()
                objects.save()
                return True
            return False
        except:
            return False
        
    
    def Uform(self, pk_pattern = "pk"):
        """
        
        Same as form(), with an object instance
        """
        try:
            key = getattr(self, pk_pattern)
            context_name = self.model_name + "_detail"
            objects = self.model.objects.filter(pk = key).get()
            self.context[context_name] = objects
            
            context_name = self.model_name + "_form"
            form = model_forms.modelform_factory(model = self.model, fields = self.field)
            form = form(**{'instance': objects})
        except:
            form = None
        self.context[context_name] = objects
        
    
    def saveUform(self, pk_pattern = "pk"):
        """
        
        Same as saveform(), with an object instance
        """
        try:
            key = getattr(self, pk_pattern)
            objects = self.model.objects.filter(pk = key).get()
            form = model_forms.modelform_factory(model = self.model, 
                                            fields = self.fields)
            form = form(**{'data': self.request.POST, 
                            'files': self.request.FILES,
                            'instance': objects})
                            
            if form.is_valid():
                objects = form.save()
                objects.save()
            return True
        except:
            return False
            
class DisplayBase(ModelBaseView):
    
    def detail(self,  pk_pattern = "pk"):
        """
        Detail an object
            => pkey is needed.
                            
        Common suffix: "detail"
        
        Template exemple:
        
{% extends "base.html" %}

{%block content%}

<h3>{{ object1_detail.group_name }}</h3>

    <div class="col-md-12">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Objects1</th>
                </tr>
            </thead>
            <tbody>
                {% for item in object1_detail.shareholder.all %}
                    <tr>
                        <td>{{ item }}</td>
                    </tr>        
                {% endfor %}
            </tbody>
        </table>
    </div>

    <a href="{% url 'object1_list'%}">Back</a>
    </br>
    <a href="{% url 'object1_update' object1_detail.id %}">Modify</a>
    </br>
    <a href="{% url 'object1_delete' object1_detail.id %}">Delete</a>


{%endblock%}
        """
        
        context_name = self.model_name + "_detail"
        try:
            context_name = self.model_name + "_detail"
            objects = self.model.objects.filter(pk = getattr(self, pk_pattern, "pk")).get()
        except:
            objects = None
        self.context[context_name] = objects
        


    def listing(self):
        """
        List something.
                            
        Common suffix: "list"
        
        Template exemple:
        
{% extends "base.html" %}

{%block content%}

{% if object1_list %}
    <h3> Mes object1s </h3>

    <div class="col-md-12">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                </tr>
            </thead>
            <tbody>
                {% for item in object1_list %}
                    <tr>
                        <td><a href="{% url 'object1_detail' item.id %}">{{ item.group_name }}</a></td>
                    </tr>        

                {% endfor %}
            </tbody>
        </table>
    </div>

{% else %}
    <p>Sorry</p>
{% endif %}
    <a href="{% url 'object1_create' %}">Create an object1</a>
{%endblock%}
        """
        
        context_name = self.model_name + "_list"
        try:
            objects = self.model.objects.all()
        except:
            objects = None
        self.context[context_name] = objects
        
    def paginate(self, page_key = '1', nb_objects = 20, orphans = 0, empty_first_page = True):
        """
        
{% for item in objects_page %}
    {{ item.full_name|upper }}<br />
{% endfor %}

<div class="pagination">
    <span class="step-links">
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">previous</a>
        {% endif %}

        <span class="current">
            Page {{ page_obj.number }} of {{ paginator.num_pages }}.
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next</a>
        {% endif %}
    </span>
</div>
        """
        context_name = self.model_name + "_page"
        objects = self.model.objects.all()
        page_engine = Paginator(objects,
                                nb_objects,
                                orphans = orphans,
                                allow_empty_first_page = empty_first_page)
        
        if str(page_key) != 'last':
            page_number = int(page_key)
        else:
            page_number = page_engine.num_pages
            
        page = page_engine.page(page_number)
        
        
        if len(page.object_list) <= nb_objects:
            self.context.update({'paginator': None,
                                 'page_obj': None,
                                 'is_paginated': False,
                                 context_name : objects})
        else:
            self.context.update({'paginator': page_engine,
                                 'page_obj': page,
                                 'is_paginated': page.has_other_pages(),
                                 context_name : page.object_list})
                                 
class DeleteBase(ModelBaseView):
    
    def remove(self, pk_pattern = "pk"):
        
        """
        Delete an object
            => pkey is needed.
                            
        Common suffix: "confirm_delete"
        
        Template exemple:

{% extends "base.html" %}
        
{% extends "base.html" %}

    {% block content %}
        <p>Confirm delete{{ object_detail.name }}?</p>
        
        <form action="{% url "object_delete" object_detail.id %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Yes, delete." />
        <a href="{% url "object_list" %}">No, cancel</a>
        </form>

{% endblock %}
        """
        
        try:
            objects = self.model.objects.filter(pk = pk_pattern)
            objects.delete()
            return True
        except:
            return False
    
    
                                 
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
        you can add any suffix you want to it, commons ones are detailed in the doc of each fonction
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