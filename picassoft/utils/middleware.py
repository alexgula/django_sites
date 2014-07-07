from django.contrib.auth import logout


class PrettifyMiddleware(object):
    """Prettify middleware.

    Clean output of the view using Tidy."""

    options = dict(output_xhtml=True,
                   add_xml_decl=True,
                   doctype='strict',
                   indent='auto',
                   indent_spaces=4,
                   tidy_mark=False,
                   wrap=200,
                   char_encoding='utf8',
                   input_encoding='utf8')

    def process_response(self, request, response):
        import tidy # Should be moved to the module level. Is here just because Tidy package is absent, to prevent import errors.
        if response['Content-Type'].split(';', 1)[0] == 'text/html':
            content = response.content
            content = tidy.parseString(content, **self.options)
            response.content = content
        return response


class ForceInactiveUserLogoutMiddleware(object):
    """Force inactive user to logout, effectively preventing him from any authenticated user's action."""
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_active:
            logout(request)
