# coding=utf-8
import traceback
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from six import StringIO
from .data_import import load_categories
from dblog.models import Log


def get_text_from_data(dataio):
    dataio.seek(0)
    text = dataio.read().decode('utf-8-sig')
    return text


class ImportXML(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImportXML, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        dataio = None
        success = False
        message = u""
        data = u""
        try:
            if self.check_basic_auth():
                dataio = StringIO(request.read())

                load_categories(get_text_from_data(dataio))
                success = True
                message = u"Успешно загружены данные из 1С."

                return HttpResponse("success")
            else:
                error_message = u"Ошибка загрузки данных из 1С: неправильное имя пользователя или пароль."
                auth_message = u"HTTP_AUTHORIZATION: " + self.request.META.get('HTTP_AUTHORIZATION', ' ')
                success = False
                message = u"\n".join([error_message, auth_message])
                return HttpResponse("failure", status=401)
        except Exception as e:
            if transaction.is_dirty():
                transaction.rollback()
            success = False
            message = u"\n".join([u"Ошибка загрузки данных из 1С:", traceback.format_exc()])
            if dataio:
                data = get_text_from_data(dataio)
                dataio.close()
            raise
        finally:
            with transaction.commit_on_success():
                Log.objects.create(success=success, message=message, data=data)

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
