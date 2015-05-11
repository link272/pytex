from django.core.paginator import Paginator

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