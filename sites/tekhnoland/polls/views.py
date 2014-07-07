from django.db.models.expressions import F
from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.views.generic.base import View
from .models import Poll, Answer


class Vote(View):

    def post(self, request, poll_id):
        if request.user.is_authenticated():
            poll = get_object_or_404(Poll, pk=poll_id)
            try:
                choice_pk = request.POST['choice']
                Answer.objects.create(poll=poll, choice_id=choice_pk, customer=request.user)
            except (KeyError, IntegrityError):
                pass
            else:
                poll.choice_set.filter(pk=choice_pk).update(votes=F('votes')+1)

        return HttpResponseRedirect(request.POST['next'])
