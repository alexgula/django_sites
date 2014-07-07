# coding=utf-8
from datetime import datetime, timedelta
from django import http
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View, TemplateView, ListView, CreateView, FormView
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from picassoft.utils.classviews import JSONResponseMixin
from ..navigation.models import StaticNode
from ..navigation.views import HomeNavigationMixin
from .models import Author, Contest, Photo, Vote, RegistrationException, ActivationKeyException
from .forms import AuthorRegistrationForm, AuthorAuthenticationForm, PhotoUploadForm
from .email import send_activation_email
from .auth import author_login, author_logout


ORDER_TO_FIELD_MAP = {
    'post': 'post_date',
    'author': 'author__name',
    'votes': 'votes',
}


def map_order_to_field_name(order):
    if order is None:
        return None
    if order[0] == '-':
        return '-' + ORDER_TO_FIELD_MAP.get(order[1:])
    else:
        return ORDER_TO_FIELD_MAP.get(order)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class PhotoContestNavigationMixin(HomeNavigationMixin):
    trail = None

    def get_trail_nodes(self):
        trail = super(PhotoContestNavigationMixin, self).get_trail_nodes()
        trail.append(StaticNode(_("Photo Contest"), 'photocontest_list'))
        if self.trail:
            trail.append(self.trail)
        return trail


class PhotoContestList(PhotoContestNavigationMixin, ListView):
    model = Photo

    def get(self, request, *args, **kwargs):
        self.sort_order = request.GET.get('order')
        self.current_site = get_current_site(request)
        return super(PhotoContestList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhotoContestList, self).get_context_data(**kwargs)
        context['sort_order'] = self.sort_order
        context['contest'] = self.contest
        context['site'] = self.current_site
        return context

    def get_queryset(self):
        queryset = super(PhotoContestList, self).get_queryset()

        self.contest = Contest.objects.active()

        queryset = queryset.filter(contest=self.contest).filter(active=True)

        field_name = map_order_to_field_name(self.sort_order)
        if field_name is not None:
            queryset = queryset.order_by(field_name)

        return queryset


class PhotoContestRegister(PhotoContestNavigationMixin, CreateView):
    model = Author
    form_class = AuthorRegistrationForm
    success_url = reverse_lazy('photocontest_list')
    template_name = 'photocontest/register_form.html'
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Register"), 'photocontest_register')

    def form_valid(self, form):
        # Call super to initialize self.object
        result = super(PhotoContestRegister, self).form_valid(form)
        send_activation_email(self.request, self.object)
        messages.info(self.request, _("To finish registration, please follow the activation link sent to your email."))
        return result


class PhotoContestRegisterConfirm(PhotoContestNavigationMixin, TemplateView):
    template_name = 'photocontest/register_error.html'
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Register"), 'photocontest_register_confirm')

    def get(self, request, *args, **kwargs):
        activation_key = kwargs['activation_key']
        try:
            Author.objects.activate(activation_key)
        except (RegistrationException, ActivationKeyException), e:
            return super(PhotoContestRegisterConfirm, self).get(request, *args, error=e)
        messages.success(request, _("Congratulations! You have succesfully registered!"))
        return redirect('photocontest_list')


class PhotoContestLogin(PhotoContestNavigationMixin, FormView):
    template_name = 'photocontest/login_form.html'
    form_class = AuthorAuthenticationForm
    success_url = reverse_lazy('photocontest_list')
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Login"), 'photocontest_login')

    def form_valid(self, form):
        author_login(self.request, form.get_author())
        messages.success(self.request, _("Now you can add some photo..."))
        return super(PhotoContestLogin, self).form_valid(form)


class PhotoContestLogout(PhotoContestNavigationMixin, View):
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Logout"), 'photocontest_logout')

    def get(self, request, *args, **kwargs):
        author_logout(request)
        return redirect('photocontest_list')


class PhotoContestUpload(PhotoContestNavigationMixin, CreateView):
    model = Photo
    form_class = PhotoUploadForm
    success_url = reverse_lazy('photocontest_list')
    template_name = 'photocontest/upload_form.html'
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Upload"), 'photocontest_upload')

    def get(self, request, *args, **kwargs):
        if not request.author:
            return redirect('photocontest_list')
        return super(PhotoContestUpload, self).get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not request.author:
            return redirect('photocontest_list')
        return super(PhotoContestUpload, self).post(self, request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PhotoContestUpload, self).get_form_kwargs()
        kwargs['author'] = self.request.author
        return kwargs


class PhotoContestTerms(PhotoContestNavigationMixin, TemplateView):
    #trail_parent = PhotoContestList
    trail = StaticNode(_("Terms"), 'photocontest_terms')

    def get_template_names(self):
        return [
            'photocontest/terms_{}.html'.format(self.request.LANGUAGE_CODE),
            'photocontest/terms.html'
        ]


class PhotoContestVote(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, id=(request.POST['id']))
        client_ip = get_client_ip(request)
        yesterday = datetime.now() - timedelta(days=1)

        if not request.user.is_superuser and Vote.objects.filter(
                photo=photo, address=client_ip, post_date__gte=yesterday).exists():
            return http.HttpResponseForbidden()

        vote = Vote(photo=photo, address=client_ip)
        vote.save()
        photo.votes = Vote.objects.filter(photo=photo).count()
        photo.save()
        return self.render_to_response({'votes': photo.votes})
