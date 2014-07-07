from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.http import HttpResponse
from hpb.news.models import OneNew

def one_news_list(request):
    news = OneNew.objects.all()
    t = loader.get_template("one_news_list.html")
    c = RequestContext(request, {'object_list': news})
    return HttpResponse(t.render(c))

def one_news_details(request,news_id):
    news = get_object_or_404(OneNew, id=news_id)
    t = loader.get_template("one_news_details.html")
    c = RequestContext(request, {'object': news})
    return HttpResponse(t.render(c))
