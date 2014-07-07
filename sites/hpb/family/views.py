from django.shortcuts import get_object_or_404
from django.template import loader, RequestContext
from django.http import HttpResponse
from .models import FamilyMember, Gallery

def family_member_list(request):
    members = FamilyMember.objects.exclude(id=4)
    t = loader.get_template("family_member_list.html")
    c = RequestContext(request, {'object_list': members})
    return HttpResponse(t.render(c))

def family_member_details(request, member_id):
    member = get_object_or_404(FamilyMember, id=member_id)
    t = loader.get_template("family_member_details.html")
    c = RequestContext(request, {'object': member})
    return HttpResponse(t.render(c))

def epbpage(request):
    member = get_object_or_404(FamilyMember, id=4)
    gallery = Gallery.objects.all()
    t = loader.get_template("epb_page.html")
    c = RequestContext(request, {'object': member, 'gallery': gallery})
    return HttpResponse(t.render(c))
