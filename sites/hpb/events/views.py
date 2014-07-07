from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Event

def event_list(request):
    events = Event.objects.all()
    t = loader.get_template("event_list.html")
    c = RequestContext(request, {'object_list': events})
    return HttpResponse(t.render(c))

def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    t = loader.get_template("event_details.html")
    c = RequestContext(request, {'object': event})
    return HttpResponse(t.render(c))
