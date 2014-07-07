# coding=utf-8
import os
from cStringIO import StringIO
import traceback
from django.conf import settings
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .data_import import load
from .models import Log
from picassoft.utils.files import safe_make_dirs


class ImportXML(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImportXML, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        dataio = None
        try:
            if self.check_basic_auth():
                dataio = StringIO(request.read())

                # Due to the strange behaviour of Django Request (or WSGI), first line of the request is '\r\n'.
                # Seems to be the specific problem of the development server.
                # To circumvent this just read first line. If everything is ok and first line starts with
                # XML declaration, just seek back to the beginning.
                if dataio.readline().startswith('<?xml'):
                    dataio.seek(0)

                load(dataio)
                Log.objects.create(results=u"Успешно загружены данные из 1С.")

                safe_make_dirs(settings.TMP_ROOT, 0755)
                dataio.seek(0)
                with open(os.path.join(settings.TMP_ROOT, 'interop.xml'), 'w') as last_data:
                    last_data.write(dataio.read())
                return HttpResponse("success")
            else:
                error_message = u"Ошибка загрузки данных из 1С: неправильное имя пользователя или пароль."
                auth_message = u"HTTP_AUTHORIZATION: " + self.request.META.get('HTTP_AUTHORIZATION', ' ')
                error_message = u"\n".join([error_message, auth_message])
                Log.objects.create(results=error_message, success=False)
                return HttpResponse("failure", status=401)
        except Exception:
            transaction.rollback()
            error_message = u"\n".join([u"Ошибка загрузки данных из 1С:", traceback.format_exc()])
            if dataio:
                dataio.seek(0)
                data = unicode(dataio.read(), 'windows-1251', errors='replace')
            else:
                data = u""
            with transaction.commit_on_success():
                Log.objects.create(results=error_message, success=False, data=data)
            raise
        finally:
            if dataio:
                dataio.close()

    def check_basic_auth(self):
        username, password = self.get_basic_auth()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return False
        return user.is_active and user.check_password(password)

    def get_basic_auth(self):
        authentication = self.request.META.get('HTTP_AUTHORIZATION', ' ')
        authmethod, auth = authentication.split(' ',1)
        if 'basic' == authmethod.lower():
            return auth.strip().decode('base64').split(':',1)
        else:
            return None, None
