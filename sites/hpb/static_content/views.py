from django.shortcuts import render_to_response
from django.template.context import RequestContext

def content(request, template_name):
    template_names = [
        #'static_content/{}_{}.html'.format(template_name, request.LANGUAGE_CODE),
        'static_content/{}.html'.format(template_name)
    ]
    return render_to_response(template_names, context_instance=RequestContext(request))
