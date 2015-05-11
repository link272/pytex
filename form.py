#-*- coding : utf-8 -*-
from base import ModelBaseView
from django.forms import models as model_forms

class FormBase(ModelBaseView):
    
    """
    Views based on form
        
    """
    fields = None
    
    def form(self):
        
        """
        
        create a Form to be sent to the client
                            
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