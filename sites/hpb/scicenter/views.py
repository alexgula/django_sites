# coding=utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Page

def page_list(request):
    pages = Page.objects.filter(active=True)
    return render_to_response("scicenter_page.html", {'object_list': pages}, context_instance=RequestContext(request))
