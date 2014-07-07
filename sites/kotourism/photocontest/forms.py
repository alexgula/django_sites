# coding=utf-8
from django import forms
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _
from .models import Author, Contest, Photo, HELPTEXT_REQUIRED
from .auth import author_authenticate


class AuthorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'required'}),
        label=_("Password"),
        help_text=HELPTEXT_REQUIRED.format(128))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'required'}),
        label=_("Repeat password"),
        help_text=HELPTEXT_REQUIRED.format(128))

    class Meta:
        model = Author
        fields = ('email', 'password1', 'password2', 'name', 'phone')

    def clean_email(self):
        email = self.cleaned_data['email']

        authors = list(Author.objects.filter(email=email).all())
        # Not yet registered
        if len(authors) == 0:
            return email

        author = authors[0]
        # Author was registered but not active (not confirmed probably)
        if author.activation_key_expired():
            author.delete()
            return email

        raise forms.ValidationError(_("Author with the same e-mail is already registered"))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("Entered passwords are not equal"))
            self.instance.password = make_password(self.cleaned_data['password1'])
        return self.cleaned_data


class AuthorAuthenticationForm(forms.Form):
    email = forms.CharField(label=_("Email"), max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _("Please enter a correct email and password. "
                           "Note that both fields may be case-sensitive."),
        'no_cookies': _("Your Web browser doesn't appear to have cookies "
                        "enabled. Cookies are required for logging in."),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.author_cache = None
        super(AuthorAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.author_cache = author_authenticate(email, password)
            if self.author_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'])
            elif not self.author_cache.active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_author(self):
        return self.author_cache


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('name', 'image', )

    def __init__(self, author,  *args, **kwargs):
        self.author = author
        self.contest = Contest.objects.active()
        super(PhotoUploadForm, self).__init__(*args, **kwargs)

    def clean(self):
        self.instance.author = self.author
        self.instance.contest = self.contest

        return self.cleaned_data
