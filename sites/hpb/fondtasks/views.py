# coding=utf-8
from django.template import loader, RequestContext
from django.http import HttpResponse
from .models import FondTask

def fondtask_list(request):
    members = FondTask.objects.all()
    t = loader.get_template("fond_task.html")
    c = RequestContext(request, {'object_list': members})
    return HttpResponse(t.render(c))
